page_base = 'https://www.thatch.co/sellers/all'
start_page = 100
end_page = 200 
page_urls = [f'{page_base}?page={page}' for page in range(start_page, end_page + 1)]


print(page_urls)