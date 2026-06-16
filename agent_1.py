from typing import Optional
from playwright.sync_api import sync_playwright
import os, time
from chatbot import get_answer


def read_webpage(url: Optional[str], output_path: str, *,timeout: int = 10000):
		"""Navigate to `url` with Playwright, extract the DOM hierarchy with element-level texts,
		and write the resulting text hierarchy to `output_path`.

		If `url` is None an exception will be raised by the caller — callers can read it from
		`config.py` and pass it in.
		"""

		def _node_text_lines(node, level=0):
			if not node:
				return []
			lines = []
			text = (node.get('text') or '').strip()
			if text:
				lines.append('\t' * level + text)
			child_level = level + 1 if text else level
			for child in node.get('children', []):
				lines.extend(_node_text_lines(child, child_level))
			return lines
		if not url:
				raise ValueError("A URL must be provided to fetch the webpage.")

		js_walk = r"""
		() => {
			function normalizeText(text){
				return text.replace(/\s+/g,' ').trim();
			}
			function walk(el){
				if(el.nodeType !== 1) return null;
				var entries = [];
				for(var i=0;i<el.childNodes.length;i++){
					var n = el.childNodes[i];
					if(n.nodeType===3){
						var text = normalizeText(n.textContent);
						if(text) entries.push({ type: 'text', text: text });
					} else if(n.nodeType===1){
						var child = walk(n);
						if(child) entries.push({ type: 'node', node: child });
					}
				}
				var text = '';
				var children = [];
				for(var j=0;j<entries.length;j++){
					if(entries[j].type === 'text'){
						if(text === ''){
							text = entries[j].text;
						} else {
							children.push({ text: entries[j].text, children: [] });
						}
					} else {
						children.push(entries[j].node);
					}
				}
				if(!text && children.length === 0) return null;
				return { text: text, children: children };
			}
			return walk(document.body);
		}
		"""

		os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

		with sync_playwright() as p:
			browser = p.chromium.launch(headless=True)
			page = browser.new_page()
			page.goto(url, wait_until="domcontentloaded")
			page.wait_for_selector('body', timeout=timeout)
			clicked = False
			try:
				page.locator('span:has-text("Reject all")').first.click(timeout=5000)
				clicked = True
			except:
				pass

			# Try a set of common reject/decline consent buttons across different sites.
			reject_texts = [
				"Reject all",
				"Reject",
				"Decline",
				"Deny",
				"Do not accept",
				"Reject cookies",
				"Decline all",
				"Reject optional",
				"Only essential",
				"Manage preferences",
			]
			selectors = [
				'button',
				'span',
				'a',
				'div',
				'[role="button"]',
				'input[type="button"]',
				'input[type="submit"]',
				'[id*="reject"]',
				'[id*="decline"]',
				'[id*="cookie"]',
				'[class*="reject"]',
				'[class*="decline"]',
				'[class*="cookie"]',
				'[aria-label*="reject"]',
				'[aria-label*="decline"]',
				'[aria-label*="cookie"]',
			]

			clicked = False
			for text in reject_texts:
				if clicked:
					break
				for selector in selectors:
					try:
						locator = page.locator(f'{selector}:has-text("{text}")').first
						if locator.count(timeout=0) > 0:
							locator.click(timeout=0)
							clicked = True
							break
					except Exception:
						pass
				if clicked:
					break

			time.sleep(5)

			data = page.evaluate(js_walk)
			browser.close()
		
		removed_lines = ['{', '}', 'cookies', 'consent', 'privacy', 'policy', 'terms', 'accept', 'decline', 'reject']
		text_lines = [line for line in _node_text_lines(data) if not any(removed_line in line for removed_line in removed_lines)]
		text_output = '\n'.join(text_lines).replace('•', '\n')
		with open(output_path, 'w', encoding='utf-8') as f:
			f.write(text_output)

		return output_path


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
webpage_path = 'webpage.txt'
read_webpage(url, webpage_path)


with open('inputs/agent_1_prompt.txt') as f:
    prompt = f.read()

with open(webpage_path) as f:
    webpage = f.read()

prompt = prompt.replace('[PASTE RAW TEXT HERE]', webpage)
#answer = get_answer(prompt)