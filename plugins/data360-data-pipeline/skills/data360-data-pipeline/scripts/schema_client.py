"""Read-only Data 360 Connect metadata client; never expose authentication payloads."""
import json
import re
import subprocess
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def authenticate_to_org(org_alias):
    try:
        result = subprocess.run(
            ['sf', 'org', 'display', '--target-org', org_alias, '--json'],
            capture_output=True, text=True, check=True, timeout=60)
        data = json.loads(result.stdout)
        if data.get('status') != 0:
            raise ValueError('Authentication failed')
        info = data['result']
        if info.get('connectedStatus') != 'Connected':
            raise ValueError('Org is not connected')
        instance = info['instanceUrl']
        parsed = urlsplit(instance)
        if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError('Invalid instance URL')
        token = info['accessToken']
        if not isinstance(token, str) or not token:
            raise ValueError('Missing access token')
        return instance.rstrip('/'), token, info.get('username', 'Unknown')
    except (subprocess.SubprocessError, OSError, ValueError, KeyError, TypeError):
        # stdout/stderr and exception strings may contain tokens; do not echo them.
        raise RuntimeError('Unable to authenticate selected org; check SF CLI login and alias.') from None


def metadata_path(api_version, collection):
    if not re.fullmatch(r'v[0-9]+\.0', api_version):
        raise ValueError('API version must use vNN.0 format')
    if collection not in ('data-lake-objects', 'data-model-objects'):
        raise ValueError('Unsupported metadata collection')
    return f'/services/data/{api_version}/ssot/{collection}'


def get_json(instance_url, token, path):
    url = urljoin(instance_url + '/', path)
    base, target = urlsplit(instance_url), urlsplit(url)
    if (base.scheme != 'https' or target.scheme != 'https' or
            target.netloc != base.netloc or target.username or target.password or
            target.fragment or not target.path.startswith('/services/data/')):
        raise ValueError('Refusing metadata URL outside the selected org')
    request = Request(url, headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json'})
    try:
        with build_opener(NoRedirects()).open(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f'Metadata request failed (HTTP {exc.code}); inspect permissions and API compatibility.') from None
    except (URLError, TimeoutError, ValueError):
        raise RuntimeError('Metadata request failed or returned invalid JSON.') from None


def list_collection(instance_url, token, api_version, collection, key):
    endpoint = metadata_path(api_version, collection)
    path = endpoint + '?' + urlencode({'limit': 50, 'orderBy': 'ASC'})
    result, visited, identities = [], set(), set()
    for _ in range(1000):
        absolute = urljoin(instance_url + '/', path)
        parsed = urlsplit(absolute)
        if parsed.path != endpoint:
            raise ValueError('Pagination changed the metadata endpoint')
        if absolute in visited:
            raise RuntimeError('Pagination loop; results are incomplete')
        visited.add(absolute)
        payload = get_json(instance_url, token, path)
        if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
            raise RuntimeError('Unexpected metadata response; refusing to report an empty inventory')
        batch = payload[key]
        for item in batch:
            if not isinstance(item, dict):
                raise RuntimeError('Invalid metadata object')
            identity = (item.get('id') or item.get('name'), item.get('dataSpaceName'))
            if identity[0] is None or identity in identities:
                raise RuntimeError('Missing or repeated metadata identity; results are incomplete')
            identities.add(identity)
        result.extend(batch)
        next_page = payload.get('nextPageUrl')
        if next_page:
            if not isinstance(next_page, str):
                raise RuntimeError('Invalid pagination URL')
            path = urljoin(absolute, next_page)
            continue
        total = payload.get('totalSize')
        if total is not None and (type(total) is not int or total < len(result)):
            raise RuntimeError('Inconsistent metadata total; rerun the inventory')
        if total is not None and len(result) >= total:
            return result
        if total is None and len(batch) < 50:
            return result
        if not batch:
            raise RuntimeError('Incomplete metadata pagination')
        # Older responses can omit nextPageUrl. Use the documented offset contract.
        path = endpoint + '?' + urlencode({'limit': 50, 'offset': len(result), 'orderBy': 'ASC'})
    raise RuntimeError('Pagination safety limit reached; results are incomplete')
