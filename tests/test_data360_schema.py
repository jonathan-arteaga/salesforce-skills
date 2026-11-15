"""Offline regressions for complete metadata inventories and credential boundaries."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError

SCRIPTS = Path(__file__).resolve().parents[1]/'plugins/data360-schema-get/skills/data360-schema-get/scripts'
spec = importlib.util.spec_from_file_location('schema_client', SCRIPTS/'schema_client.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class SchemaClientTests(unittest.TestCase):
    def inventory(self):
        return c.list_collection('https://example.my.salesforce.com', 'secret', 'v64.0', 'data-model-objects', 'dataModelObject')

    def test_collects_multiple_pages(self):
        pages = [{'dataModelObject': [{'name':'A'}], 'nextPageUrl':'/services/data/v64.0/ssot/data-model-objects?offset=1'},
                 {'dataModelObject': [{'name':'B'}], 'totalSize':2}]
        with patch.object(c, 'get_json', side_effect=pages) as get:
            self.assertEqual([r['name'] for r in self.inventory()], ['A','B'])
            self.assertEqual(get.call_count, 2)

    def test_offset_fallback(self):
        pages = [{'dataModelObject':[{'name':'A'}], 'totalSize':2}, {'dataModelObject':[{'name':'B'}], 'totalSize':2}]
        with patch.object(c, 'get_json', side_effect=pages) as get:
            self.assertEqual(len(self.inventory()), 2)
            self.assertIn('offset=1', get.call_args.args[2])

    def test_short_final_page_without_total(self):
        with patch.object(c,'get_json',return_value={'dataModelObject':[{'name':'A'}]}):
            self.assertEqual(len(self.inventory()),1)

    def test_dlo_key(self):
        with patch.object(c,'get_json',return_value={'dataLakeObjects':[{'name':'A__dll'}],'totalSize':1}):
            self.assertEqual(len(c.list_collection('https://example.my.salesforce.com','secret','v64.0','data-lake-objects','dataLakeObjects')),1)

    def test_malformed_response_is_not_empty_success(self):
        for data in [{}, [], {'dataModelObject':None}, {'dataModelObject':['bad']}, {'dataModelObject':[{}]}]:
            with self.subTest(data=data), patch.object(c,'get_json',return_value=data), self.assertRaises(RuntimeError):self.inventory()

    def test_duplicate_or_loop_fails(self):
        with patch.object(c,'get_json',return_value={'dataModelObject':[{'name':'A'}],'totalSize':3}), self.assertRaises(RuntimeError):self.inventory()
        page={'dataModelObject':[{'name':'A'}],'nextPageUrl':'?limit=50&orderBy=ASC'}
        with patch.object(c,'get_json',return_value=page), self.assertRaises(RuntimeError):self.inventory()

    def test_incomplete_total_fails(self):
        with patch.object(c,'get_json',return_value={'dataModelObject':[],'totalSize':2}), self.assertRaises(RuntimeError):self.inventory()

    def test_pagination_cannot_change_endpoint(self):
        page={'dataModelObject':[{'name':'A'}],'nextPageUrl':'/services/data/v64.0/query'}
        with patch.object(c,'get_json',return_value=page), self.assertRaises(ValueError):self.inventory()

    def test_cross_origin_and_http_rejected_before_network(self):
        for path in ['https://attacker.example/services/data/v64.0/ssot/data-model-objects','http://example.my.salesforce.com/services/data/v64.0/ssot/data-model-objects','//attacker.example/path','/other']:
            with self.subTest(path=path), patch.object(c,'build_opener') as opener, self.assertRaises(ValueError):
                c.get_json('https://example.my.salesforce.com','secret',path)
            opener.assert_not_called()

    def test_redirects_disabled(self):
        self.assertIsNone(c.NoRedirects().redirect_request(None,None,302,'',{},'https://attacker.example'))

    def test_http_errors_do_not_echo_body(self):
        opener=MagicMock();opener.open.side_effect=HTTPError('https://example.my.salesforce.com',403,'secret',{},io.BytesIO(b'secret'))
        with patch.object(c,'build_opener',return_value=opener), self.assertRaises(RuntimeError) as error:
            c.get_json('https://example.my.salesforce.com','secret','/services/data/v64.0/ssot/data-model-objects')
        self.assertIn('403',str(error.exception));self.assertNotIn('secret',str(error.exception))

    def test_auth_failure_does_not_echo_token(self):
        failures=[subprocess.CalledProcessError(1,['sf'],output='secret',stderr='secret'),subprocess.TimeoutExpired(['sf'],60)]
        for failure in failures:
            with patch.object(c.subprocess,'run',side_effect=failure), self.assertRaises(RuntimeError) as error:c.authenticate_to_org('demo')
            self.assertNotIn('secret',str(error.exception))

    def test_auth_success_captures_without_printing(self):
        payload={'status':0,'result':{'connectedStatus':'Connected','instanceUrl':'https://example.my.salesforce.com','accessToken':'secret','username':'demo'}}
        with patch.object(c.subprocess,'run',return_value=MagicMock(stdout=json.dumps(payload))), patch('sys.stdout',new_callable=io.StringIO) as output:
            self.assertEqual(c.authenticate_to_org('demo')[1],'secret');self.assertEqual(output.getvalue(),'')

    def test_wrappers_load_and_call_shared_client(self):
        with patch.dict(sys.modules,{'schema_client':c}):
            for kind,key in [('dlo','dataLakeObjects'),('dmo','dataModelObject')]:
                spec=importlib.util.spec_from_file_location('get_'+kind,SCRIPTS/('get_'+kind+'_schema.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                with patch.object(c,'get_json',return_value={key:[{'name':'A'}],'totalSize':1}):
                    self.assertEqual(len(getattr(module,'list_all_'+kind+'s')('https://example.my.salesforce.com','secret')),1)
                with patch.object(module,'get_json',return_value={'name':'A'}) as get:
                    getattr(module,'get_'+kind+'_schema')('https://example.my.salesforce.com','secret','A/B')
                    self.assertTrue(get.call_args.args[2].endswith('A%2FB'))
                with patch.object(module,'authenticate_to_org',return_value=('https://example.my.salesforce.com','secret','demo')), patch.object(module,'get_'+kind+'_schema',return_value={'name':'A'}) as schema, patch.object(module,'list_all_'+kind+'s') as inventory, patch.object(module,'display_'+kind+'_schema'), patch.object(sys,'argv',['schema','demo','A','--api-version','v68.0']):
                    self.assertEqual(module.main(),0)
                    self.assertEqual(schema.call_args.args[-1],'v68.0')
                    inventory.assert_not_called()


if __name__=='__main__':unittest.main()
