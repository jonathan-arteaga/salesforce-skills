#!/usr/bin/env python3
"""
List all Data Model Objects and retrieve schema for one DMO using REST API.
Uses SF CLI for authentication.
"""

import json
import sys
from urllib.parse import quote
from schema_client import authenticate_to_org, get_json, list_collection, metadata_path


def list_all_dmos(instance_url, access_token, api_version='v64.0'):
    """Return the complete visible metadata collection or fail explicitly."""
    return list_collection(instance_url, access_token, api_version,
                           'data-model-objects', 'dataModelObject')


def get_dmo_schema(instance_url, access_token, dmo_name, api_version='v64.0'):
    path = metadata_path(api_version, 'data-model-objects')
    result = get_json(instance_url, access_token, path + '/' + quote(dmo_name, safe=''))
    if not isinstance(result, dict):
        raise RuntimeError('Unexpected schema response')
    return result


def display_dmo_list(dmos):
    """Display summary of all DMOs."""
    print("=" * 80)
    print("📊 DATA MODEL OBJECTS")
    print("=" * 80)

    for idx, dmo in enumerate(dmos, 1):
        print(f"\n{idx}. {dmo.get('name', 'Unknown')}")
        print(f"   Label: {dmo.get('label', 'N/A')}")
        print(f"   Category: {dmo.get('category', 'N/A')}")
        print(f"   Creation Type: {dmo.get('creationType', 'N/A')}")
        print(f"   Data Space: {dmo.get('dataSpaceName', 'N/A')}")


def display_dmo_schema(dmo_detail):
    """Display detailed schema information for a DMO."""
    print("\n" + "=" * 80)
    print(f"🔍 SCHEMA DETAILS FOR: {dmo_detail.get('name')}")
    print("=" * 80)

    print(f"\n📝 Basic Information:")
    print(f"   Name: {dmo_detail.get('name')}")
    print(f"   Label: {dmo_detail.get('label')}")
    print(f"   Category: {dmo_detail.get('category')}")
    print(f"   Creation Type: {dmo_detail.get('creationType', 'N/A')}")
    print(f"   Data Space: {dmo_detail.get('dataSpaceName', 'N/A')}")

    # Display field schema
    fields = dmo_detail.get('fields', [])

    if fields:
        print(f"\n🔧 Fields ({len(fields)} total):")
        print("-" * 80)

        # Show all fields with detailed info
        for field in fields:
            print(f"\n   • {field.get('name')}")
            print(f"     Label: {field.get('label', 'N/A')}")
            print(f"     Data Type: {field.get('type', 'Unknown')}")
            print(f"     Primary Key: {field.get('isPrimaryKey', False)}")
            print(f"     Creation Type: {field.get('creationType', 'N/A')}")
            print(f"     Usage Tag: {field.get('usageTag', 'N/A')}")

            if 'length' in field:
                print(f"     Length: {field['length']}")
            if 'precision' in field:
                print(f"     Precision: {field['precision']}")
            if 'scale' in field:
                print(f"     Scale: {field['scale']}")
    else:
        print("\n   ⚠️  No fields found in schema")

    # Show full JSON
    print("\n" + "=" * 80)
    print("📄 FULL SCHEMA (JSON):")
    print("=" * 80)
    print(json.dumps(dmo_detail, indent=2))


def main():
    """Read only the selected schema or a complete visible inventory."""
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('org_alias')
    parser.add_argument('object_name', nargs='?')
    parser.add_argument('--api-version', default='v64.0', help='Verified target API version, e.g. v68.0; default v64.0')
    args = parser.parse_args()
    try:
        metadata_path(args.api_version, 'data-model-objects')
        instance_url, access_token, _ = authenticate_to_org(args.org_alias)
        if args.object_name:
            detail = get_dmo_schema(instance_url, access_token, args.object_name, args.api_version)
            display_dmo_schema(detail)
        else:
            objects = list_all_dmos(instance_url, access_token, args.api_version)
            display_dmo_list(objects)
            print(f"Visible DMO count: {len(objects)}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
