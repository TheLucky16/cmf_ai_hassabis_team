k = 1
urls = [
    "https://www.youtube.com/@CMF_YNVRSTY/videos",
    "https://www.coursera.org/learn/wharton-quantitative-modeling",
    "https://www.khanacademy.org/economics-finance-domain/core-finance/money-and-banking",
    "https://www.london.edu/executive-education/digital-transformation-and-innovation/analytics-and-ai-from-data-insights-to-strategic-impact?utm_source=google&utm_medium=ppc&utm_campaign=MC_EEAAI_ppc_google&utm_content=ppc&gclsrc=aw.ds&&ppc_keyword=data%20analyst%20course&gad_source=1&gad_campaignid=21136873610&gbraid=0AAAAADkMszMPB_O5QzkF7hJpcAAY9vxsD&gclid=EAIaIQobChMIjIqBxdXylAMVXJdQBh3mlAvpEAAYAiAAEgKbc_D_BwE",
    "https://www.insead.edu/executive-education/lp/financial-analysis-managers-online?CampaignId=GGL_Search_A&SiteId=GGL&CampaignName=EUR-IE[EN]_GGL-NonBrand[GEN]-EDP-FinancialAnalysis_MT-Phrase&AdId=FAN&device=c&term=financial%20analyst%20course_(p)&utm_medium=cpc&gad_source=1&gad_campaignid=11488428840&gbraid=0AAAAAD6tgXx0WDD8KlmTgeUKc4Ay3APAk&gclid=EAIaIQobChMIjIqBxdXylAMVXJdQBh3mlAvpEAAYAyAAEgLYjvD_BwE",
    "https://www.cfainstitute.org/programs/cfa-program?s_cid=cpc-nl1_msq-global-row-fy26-generic-prospecting-b2c-SFDCDirect701KZ0000002kN9YAI-googleads-demand_gen-all-x-financial%20analyst%20course-earlyreg-lmf&gclsrc=aw.ds&gad_source=1&gad_campaignid=21171128321&gbraid=0AAAAAocOZ1kzMa-sDdKIfzWr-aGo9sBOQ&gclid=EAIaIQobChMIjIqBxdXylAMVXJdQBh3mlAvpEAAYBCAAEgLbXPD_BwE",
]
url = urls[k]
headless = True 

# free token gotten from: https://openrouter.ai/openrouter/owl-alpha
or_token_path = "/Users/thelucky16/Documents/or_api.txt"
stage_2_prompt = 'You are a curriculum extractor. Return JSON only. For each educational topic found, create a lesson. Ignore: - navigation - footer - cookie notices - login text Output: {"lessons": [ { "title": "", "description": "","estimated_minutes": 0,"keywords": []}]}'
model = "openrouter/owl-alpha"



