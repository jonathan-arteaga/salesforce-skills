#!/usr/bin/env python3
"""
List all Data Lake Objects and retrieve schema for one DLO using REST API.
Uses SF CLI for authentication.
"""

import json
import sys
from urllib.parse import quote
from schema_client import authenticate_to_org, get_json, list_collection, metadata_path


def list_all_dlos(instance_url, access_token, api_version='v64.0'):
    """Return the complete visible metadata collection or fail explicitly."""
    return list_collection(instance_url, access_token, api_version,
                           'data-lake-objects', 'dataLakeObjects')


def get_dlo_schema(instance_url, access_token, dlo_name, api_version='v64.0'):
    path = metadata_path(api_version, 'data-lake-objects')
    result = get_json(instance_url, access_token, path + '/' + quote(dlo_name, safe=''))
    if not isinstance(result, dict):
        raise RuntimeError('Unexpected schema response')
    if 'dataLakeObjects' in result:
        items = result['dataLakeObjects']
        if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
            raise RuntimeError('Expected exactly one DLO schema')
        return items[0]
    return result


def display_dlo_list(dlos):
    """Display summary of all DLOs."""
    print("=" * 80)
    print("📊 DATA LAKE OBJECTS")
    print("=" * 80)

    for idx, dlo in enumerate(dlos, 1):
        print(f"\n{idx}. {dlo.get('name', 'Unknown')}")
        print(f"   Label: {dlo.get('label', 'N/A')}")
        print(f"   Category: {dlo.get('category', 'N/A')}")
        if 'id' in dlo:
            print(f"   ID: {dlo['id']}")


def display_dlo_schema(dlo_detail):
    """Display detailed schema information for a DLO."""
    print("\n" + "=" * 80)
    print(f"🔍 SCHEMA DETAILS FOR: {dlo_detail.get('name')}")
    print("=" * 80)

    print(f"\n📝 Basic Information:")
    print(f"   Name: {dlo_detail.get('name')}")
    print(f"   Label: {dlo_detail.get('label')}")
    print(f"   Category: {dlo_detail.get('category')}")
    print(f"   Description: {dlo_detail.get('description', 'N/A')}")

    if 'dataspaceInfo' in dlo_detail:
        dataspaces = dlo_detail['dataspaceInfo']
        dataspace_names = [ds.get('name', 'Unknown') for ds in dataspaces]
        print(f"   Dataspaces: {', '.join(dataspace_names)}")

    # Display field schema
    fields = dlo_detail.get('fields', [])

    if fields:
        print(f"\n🔧 Fields ({len(fields)} total):")
        print("-" * 80)

        # Show all fields with detailed info
        for field in fields:
            print(f"\n   • {field.get('name')}")
            print(f"     Label: {field.get('label', 'N/A')}")
            print(f"     Data Type: {field.get('dataType', 'Unknown')}")
            print(f"     Primary Key: {field.get('isPrimaryKey', False)}")
            print(f"     Nullable: {field.get('isNullable', True)}")

            if 'length' in field:
                print(f"     Length: {field['length']}")
            if 'precision' in field:
                print(f"     Precision: {field['precision']}")
            if 'scale' in field:
                print(f"     Scale: {field['scale']}")
    else:
        print("\n   ⚠️  No fields found in schema")

    # Show full JSON (optional, can be commented out)
    print("\n" + "=" * 80)
    print("📄 FULL SCHEMA (JSON):")
    print("=" * 80)
    print(json.dumps(dlo_detail, indent=2))


def main():
    """Read only the selected schema or a complete visible inventory."""
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('org_alias')
    parser.add_argument('object_name', nargs='?')
    parser.add_argument('--api-version', default='v64.0', help='Verified target API version, e.g. v68.0; default v64.0')
    args = parser.parse_args()
    try:
        metadata_path(args.api_version, 'data-lake-objects')
        instance_url, access_token, _ = authenticate_to_org(args.org_alias)
        if args.object_name:
            detail = get_dlo_schema(instance_url, access_token, args.object_name, args.api_version)
            display_dlo_schema(detail)
        else:
            objects = list_all_dlos(instance_url, access_token, args.api_version)
            display_dlo_list(objects)
            print(f"Visible DLO count: {len(objects)}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
