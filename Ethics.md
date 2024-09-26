## 🔍 Purpose & Ethical Considerations

The purpose of `EmpowHer` is to bring awareness to the issue of **Pink Tax** by analyzing price disparities in products marketed to women. By gathering data from Target using **Selenium**, I aimed to highlight the financial impact of gendered pricing. However, I took into consideration the importance of ethical web scraping and responsible data use.

### 🤖 Respect for `robots.txt`

Our data collection respects Target's `robots.txt` file. Please refer to Target's [robots.txt](https://www.target.com/robots.txt) for the comprehensive list. 

### 🚫 Disallowed Paths & Data Protection

Target’s `robots.txt` includes multiple disallowed paths, such as the following:

- `/Checkout`
- `/admin`
- `/AddToRegistry`
- `/custom-reviews/`
- `/tracking`
- `/social/`

These disallowed paths include areas related to user data (e.g., account or checkout information) and sensitive actions (e.g., adding items to a registry). I ensured that my scraping methods avoided these paths and adhere to Target’s policies. Data related to personal information, user accounts, and any sensitive areas were completely off-limits in this project.

### 🛠️ What Is Scraped

I only scraped product data that is publicly available on product listing pages, including:

- **Product names**
- **Prices**
- **Images**
- **Brands**

I do not scrape any personal information, user-generated content, or attempt to bypass access restrictions in any form.

### 🌍 Ethical Data Use & Transparency

I believe in using the data gathered solely for educational purposes to promote financial equality and consumer empowerment. This project does not involve redistributing scraped data for commercial purposes or violating any terms of service. The results are intended to create transparency regarding gendered pricing, empowering consumers with better information.

### 🧑‍💻 Call for Ethical Scraping

I encourage others who contribute to or fork this repository to follow the same ethical guidelines. Respect the integrity of Target’s website, adhere to the disallowed paths outlined in their `robots.txt`, and prioritize the privacy and security of user data in all activities.

**Disclaimer:** This project is a case study focused on ethical practices and consumer education. It should not be used to infringe on privacy rights or violate any legal boundaries.