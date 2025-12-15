(function() {
    // Configuration
    const EXPENSES_APP_URL = '/expenses/';
    const BUTTON_TEXT = 'تسجيل مصروف';
    const BUTTON_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>`;
    
    // Function to get current logged-in user from LocalStorage
    function getCurrentUser() {
        try {
            const userStr = localStorage.getItem('currentUser');
            if (userStr) {
                return JSON.parse(userStr);
            }
        } catch (e) {
            console.error('Manus: Failed to parse currentUser', e);
        }
        return null;
    }

    // Function to find the employee name (the one being viewed)
    function getEmployeeName() {
        // Strategy 1: Look for the specific header structure we found
        // The name is usually in an h2 with specific classes or near the email
        const possibleNames = Array.from(document.querySelectorAll('h1, h2, h3, .text-xl, .font-bold'));
        
        // Filter for elements that look like names (not system text)
        // This is heuristic-based since we don't have a specific ID
        for (let el of possibleNames) {
            const text = el.textContent.trim();
            // Avoid system labels
            if (['ملخص العهدة', 'رصيد الموظف:', 'عدد العمليات:', 'سجل العهدة', 'عملية جديدة'].includes(text)) continue;
            if (text.length < 3) continue;
            
            // Check if it has an email sibling or child, which confirms it's a user card
            const parent = el.parentElement;
            if (parent && parent.textContent.includes('@')) {
                return text;
            }
        }
        return null;
    }

    // Function to inject the button
    function injectButton() {
        // Check if button already exists
        if (document.getElementById('manus-expense-btn')) return;

        // Find the "New Operation" button to place ours next to it
        // Based on analysis: button contains text "عملية جديدة"
        const allButtons = Array.from(document.querySelectorAll('button'));
        const newOpBtn = allButtons.find(btn => btn.textContent.includes('عملية جديدة'));

        if (newOpBtn) {
            const container = newOpBtn.parentElement;
            
            // Create our button
            const expenseBtn = document.createElement('a');
            expenseBtn.id = 'manus-expense-btn';
            expenseBtn.className = newOpBtn.className.replace('from-amber-600', 'from-red-600').replace('to-orange-600', 'to-pink-600').replace('hover:from-amber-700', 'hover:from-red-700').replace('hover:to-orange-700', 'hover:to-pink-700');
            
            // If the original button has no classes (unlikely based on analysis but possible), add default styling
            if (!expenseBtn.className) {
                expenseBtn.className = "bg-gradient-to-r from-red-600 to-pink-600 text-white px-3 md:px-5 py-2 md:py-3 rounded-lg md:rounded-xl hover:from-red-700 hover:to-pink-700 flex items-center space-x-2 shadow-md transition-all w-full sm:w-auto justify-center text-sm md:text-base cursor-pointer";
            }

            expenseBtn.innerHTML = `${BUTTON_ICON} <span>${BUTTON_TEXT}</span>`;
            
            // Get employee name for the link (the profile being viewed)
            const viewedEmployeeName = getEmployeeName();
            
            // Get current logged-in user
            const currentUser = getCurrentUser();
            
            // Construct query params
            const params = new URLSearchParams();
            params.set('action', 'new_expense');
            
            if (viewedEmployeeName) {
                params.set('employee', viewedEmployeeName);
            }
            
            if (currentUser) {
                // Store current user in localStorage for the expenses app to pick up
                // This is more reliable than URL params for complex objects
                localStorage.setItem('current_user', JSON.stringify(currentUser));
                
                params.set('user_email', currentUser.email);
                params.set('user_name', currentUser.full_name);
                params.set('user_role', currentUser.role || 'user');
            }

            expenseBtn.href = `${EXPENSES_APP_URL}?${params.toString()}`;
            
            // Insert after the "New Operation" button
            container.insertBefore(expenseBtn, newOpBtn.nextSibling);
            
            console.log('Manus: Expense button injected successfully for employee:', viewedEmployeeName);
        }
    }
    
    // Also update the top navigation link to include user info
    function updateNavLink() {
        const navLink = document.querySelector('.simple-nav-link');
        if (navLink && !navLink.hasAttribute('data-user-updated')) {
            const currentUser = getCurrentUser();
            if (currentUser) {
                const currentHref = navLink.getAttribute('href');
                const separator = currentHref.includes('?') ? '&' : '?';
                const newHref = `${currentHref}${separator}user_email=${encodeURIComponent(currentUser.email)}&user_name=${encodeURIComponent(currentUser.full_name)}&user_role=${encodeURIComponent(currentUser.role || 'user')}`;
                navLink.setAttribute('href', newHref);
                navLink.setAttribute('data-user-updated', 'true');
            }
        }
    }

    // Observer to handle dynamic content loading (SPA navigation)
    const observer = new MutationObserver((mutations) => {
        injectButton();
        updateNavLink();
    });

    // Start observing
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Initial try
    setTimeout(() => {
        injectButton();
        updateNavLink();
    }, 1000);
    
    setTimeout(() => {
        injectButton();
        updateNavLink();
    }, 3000);
})();
