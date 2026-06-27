import os
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup not found. Please install it using: pip install beautifulsoup4")
    sys.exit(1)

def run_tests(file_path):
    print(f"Testing HTML file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found at {file_path}")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, 'html.parser')
    passed_tests = 0
    total_tests = 0
    
    def assert_true(condition, message):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            print(f"[PASS] {message}")
            passed_tests += 1
        else:
            print(f"[FAIL] {message}")
            
    # 1. Check Document Structure
    print("\n--- Document Structure Tests ---")
    assert_true(soup.html is not None, "HTML tag exists")
    assert_true(soup.head is not None, "Head tag exists")
    assert_true(soup.body is not None, "Body tag exists")
    
    # 2. Check Meta tags for responsiveness and SEO
    print("\n--- Meta Tags & SEO Tests ---")
    viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
    assert_true(viewport_meta is not None and 'width=device-width' in viewport_meta.get('content', ''), "Viewport meta tag exists for responsiveness")
    
    title_tag = soup.title
    assert_true(title_tag is not None and "Katasani Vijaya Lakshmi" in title_tag.text, "Title tag contains name")
    
    # 3. Check External Resources
    print("\n--- Resource Inclusions Tests ---")
    tailwind_script = soup.find('script', src=lambda s: s and 'tailwindcss.com' in s)
    assert_true(tailwind_script is not None, "Tailwind CSS CDN script included")
    
    font_awesome = soup.find('link', href=lambda h: h and 'font-awesome' in h)
    assert_true(font_awesome is not None, "FontAwesome stylesheet included")
    
    google_fonts = soup.find('link', href=lambda h: h and 'fonts.googleapis.com' in h)
    assert_true(google_fonts is not None, "Google Fonts stylesheet included")
    
    # 4. Content Tests
    print("\n--- Content & Sections Tests ---")
    # Check Name
    name_headings = soup.find_all(string=lambda t: t and "Katasani Vijaya Lakshmi" in t)
    assert_true(len(name_headings) > 0, "Name is displayed in the hero section")
    
    # Check role/tagline
    role_text = soup.find(string=lambda t: t and "Computer Science" in t and "Engineer" in t)
    assert_true(role_text is not None, "Role tagline is displayed")
    
    # Check counters
    assert_true(soup.find(string=lambda t: t and "3+" in t) is not None, "Counter: 3+ Key Projects exists")
    assert_true(soup.find(string=lambda t: t and "4" in t) is not None, "Counter: 4 Certifications exists")
    assert_true(soup.find(string=lambda t: t and "3" in t) is not None, "Counter: 3 Languages exists")
    
    # Check Sections
    sections = ['about', 'education', 'skills', 'projects', 'contact']
    for section_id in sections:
        section = soup.find('section', id=section_id)
        assert_true(section is not None, f"Section with id '{section_id}' exists")
        
    # 5. Check Projects details
    print("\n--- Projects Tests ---")
    assert_true(soup.find(string=lambda t: t and "Doctor Management System" in t) is not None, "Project 1 exists")
    assert_true(soup.find(string=lambda t: t and "UPI Fraud Detection" in t) is not None, "Project 2 exists")
    assert_true(soup.find(string=lambda t: t and "Plant Disease Prediction" in t) is not None, "Project 3 exists")
    
    # 6. Check Contacts
    print("\n--- Contact Tests ---")
    assert_true(soup.find('a', href=lambda h: h and 'github.com/Katasani-Vijayalakshmi' in h) is not None, "GitHub link exists")
    assert_true(soup.find('a', href=lambda h: h and 'linkedin.com/in/katasani-vijayalakshmi' in h) is not None, "LinkedIn link exists")
    assert_true(soup.find('a', href=lambda h: h and 'kvijaya4446@gmail.com' in h) is not None, "Email link exists")
    
    # 7. Check Navbar
    print("\n--- Navigation Tests ---")
    nav = soup.find('nav')
    assert_true(nav is not None, "Navigation bar exists")
    
    # Check sticky/fixed class
    assert_true(nav and ('fixed' in nav.get('class', []) or 'sticky' in nav.get('class', [])), "Navbar is fixed/sticky")
    
    print("\n--- Summary ---")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    
    return passed_tests == total_tests

if __name__ == '__main__':
    file_to_test = os.path.join(os.path.dirname(__file__), 'index.html')
    if run_tests(file_to_test):
        print("\nAll tests passed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed. Please review the output.")
        sys.exit(1)
