#!/usr/bin/env python3
"""Read public JLCPCB catalog data; never authenticates, reserves, orders or adds parts.

Endpoints/parameters are those used by JLCPCB's public parts-search frontend.
Only an allowlist of catalog fields is retained, excluding image signatures and
account-related fields. Stock/prices are a dated observation, not an order quote.
"""
import argparse
import concurrent.futures
import datetime
import json
from pathlib import Path
import urllib.request

API = 'https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList/v2'
FIELDS = ['componentCode', 'componentModelEn', 'componentBrandEn', 'componentSpecificationEn',
          'describe', 'stockCount', 'canPresaleNumber', 'componentLibraryType',
          'componentProductType', 'componentPrices', 'buyComponentPrices',
          'minPurchaseNum', 'preMinPurchaseNum', 'leastPatchNumber', 'lossNumber',
          'isBuyComponent', 'noBuyReason', 'allowPostFlag', 'estimateDate',
          'urlSuffix', 'dataManualUrl', 'dataManualOfficialLink', 'assemblyMode',
          'xrayFlag', 'fixtureFlag', 'orderInstructionEnglish', 'specialComponentFee']

def search(mpn):
    body = {'keyword': mpn, 'currentPage': 1, 'pageSize': 25}
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.load(response)
        if result.get('code') != 200:
            return {'query': mpn, 'error': str(result.get('code')) + ': ' + str(result.get('message'))}
        page = (result.get('data') or {}).get('componentPageInfo')
        if not isinstance(page, dict):
            return {'query': mpn, 'error': 'Catalog returned no component page; no availability inference'}
        matches = []
        for raw in page.get('list') or []:
            item = {key: raw[key] for key in FIELDS if key in raw}
            # Never retain temporary signed datasheet/image URLs.
            for key in ['dataManualUrl', 'dataManualOfficialLink']:
                if item.get(key) and 'x-oss-' in item[key]: item.pop(key)
            if item.get('urlSuffix'): item['url'] = 'https://jlcpcb.com/partdetail/' + item['urlSuffix']
            item['exact_model_match'] = item.get('componentModelEn', '').casefold() == mpn.casefold()
            matches.append(item)
        return {'query': mpn, 'total_search_matches': page['total'], 'matches': matches}
    except Exception as exc:
        return {'query': mpn, 'error': type(exc).__name__ + ': ' + str(exc)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--queries', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True); args = ap.parse_args()
    queries = json.loads(args.queries.read_text())
    if args.output.exists(): raise SystemExit('Refusing to overwrite a dated catalog capture')
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(search, queries):
            results.append(result)
            matches = result.get('matches', [])
            exact = [x for x in matches if x['exact_model_match']]
            best = sorted(exact, key=lambda x: x.get('stockCount') or 0, reverse=True)
            top = best[0] if best else {}
            print(result['query'], 'ERROR' if result.get('error') else f"total={result['total_search_matches']} exact={len(exact)}", top.get('componentCode', ''), top.get('stockCount', ''), flush=True)
    args.output.write_text(json.dumps({'captured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'endpoint': API, 'scope': 'Public unauthenticated catalog search. No reservation, account cart or order.',
        'queries': results}, indent=2) + '\n')

if __name__ == '__main__': main()
