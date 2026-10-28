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
        print(f"ERROR: File not found at {file_path}")
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
    role_text = soup.find(string=lambda t: t and "Computer Science" in t and "Engineering Graduate" in t)
    assert_true(role_text is not None, "Role tagline is displayed")
    
    # Check stats counters
    assert_true(soup.find(string=lambda t: t and "3+" in t) is not None, "Counter: 3+ Key Projects exists")
    assert_true(soup.find(string=lambda t: t and "3" in t) is not None, "Counter: 3 Certifications exists")
    assert_true(soup.find(string=lambda t: t and "2" in t) is not None, "Counter: 2 Languages exists")
    assert_true(soup.find(string=lambda t: t and "9.07" in t) is not None, "Counter: 9.07 CGPA exists")
    
    # Check Sections
    sections = ['about', 'education', 'skills', 'projects', 'certifications', 'contact']
    for section_id in sections:
        section = soup.find('section', id=section_id)
        assert_true(section is not None, f"Section with id '{section_id}' exists")
        
    # 5. Check Resume Specific Details
    print("\n--- Resume Matching Tests ---")
    # Career objective presence
    obj_text = soup.find(string=lambda t: t and "AI-based applications" in t)
    assert_true(obj_text is not None, "Career objective from resume is present")
    
    # Education
    veltech_text = soup.find(string=lambda t: t and "Vel Tech Rangarajan" in t)
    assert_true(veltech_text is not None, "Vel Tech full institution name present")
    
    # Skills: UiPath & AI/ML
    uipath_text = soup.find(string=lambda t: t and "UiPath" in t)
    assert_true(uipath_text is not None, "UiPath (RPA / Automation) present")
    
    # 6. Check Projects details from Resume
    print("\n--- Projects Tests (From Resume) ---")
    assert_true(soup.find(string=lambda t: t and "AI-Driven Smart Hiring Platform" in t) is not None, "Project 1 (AI-Driven Smart Hiring) exists")
    assert_true(soup.find(string=lambda t: t and "Candidate Matching Copilot" in t) is not None, "Project 1 subtitle exists")
    assert_true(soup.find(string=lambda t: t and "UPI Fraud Detection" in t) is not None, "Project 2 (UPI Fraud Detection) exists")
    assert_true(soup.find(string=lambda t: t and "Plant Disease Prediction" in t) is not None, "Project 3 (Plant Disease Prediction) exists")
    
    # 7. Check Certifications (3 from Resume)
    print("\n--- Certifications Tests (From Resume) ---")
    assert_true(soup.find(string=lambda t: t and "TCS iON Career Edge" in t) is not None, "TCS iON Certification exists")
    assert_true(soup.find(string=lambda t: t and "SQL and Relational Databases 101" in t) is not None, "IBM SQL Certification exists")
    assert_true(soup.find(string=lambda t: t and "Java Programming Fundamentals" in t) is not None, "Infosys Java Certification exists")

    # 8. Check Contacts
    print("\n--- Contact Tests ---")
    assert_true(soup.find('a', href=lambda h: h and 'github.com/Katasani-Vijayalakshmi' in h) is not None, "GitHub link exists")
    assert_true(soup.find('a', href=lambda h: h and 'linkedin.com/in/katasani-vijayalakshmi' in h) is not None, "LinkedIn link exists")
    assert_true(soup.find('a', href=lambda h: h and 'kvijaya4446@gmail.com' in h) is not None, "Email link exists")
    assert_true(soup.find('a', href=lambda h: h and '6301687092' in h) is not None, "Phone link exists")
    
    # 9. Check Navbar
    print("\n--- Navigation Tests ---")
    nav = soup.find('nav')
    assert_true(nav is not None, "Navigation bar exists")
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
