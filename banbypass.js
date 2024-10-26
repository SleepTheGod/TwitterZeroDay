// ==UserScript==
// @name         Block Twitter API Requests
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Block specific Twitter API requests on page load and modify headers
// @author       Taylor Christian Newsome
// @match        *://*/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    // Block Fetch requests
    const originalFetch = window.fetch;
    window.fetch = async function (...args) {
        const url = args[0];
        // Modify headers for the request
        const modifiedOptions = args[1] || {};
        modifiedOptions.headers = {
            ...modifiedOptions.headers,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://x.com/',
            'X-Requested-With': 'XMLHttpRequest',
        };

        if (typeof url === 'string' && (url.includes('twitter.com/i/api/1.1/keyregistry/register') ||
                                        url.includes('x.com/i/api/1.1/keyregistry/register') ||
                                        url.includes('api.twitter.com/i/api/1.1/keyregistry/register') ||
                                        url.includes('api.x.com/i/api/1.1/keyregistry/register'))) {
            console.log('Blocked Fetch request to:', url);
            return Promise.reject(new Error('Blocked request'));
        }
        return originalFetch.apply(this, [url, modifiedOptions]);
    };

    // Block XMLHttpRequest
    const originalXhrOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function (method, url) {
        if (url.includes('twitter.com/i/api/1.1/keyregistry/register') ||
            url.includes('x.com/i/api/1.1/keyregistry/register') ||
            url.includes('api.twitter.com/i/api/1.1/keyregistry/register') ||
            url.includes('api.x.com/i/api/1.1/keyregistry/register')) {
            console.log('Blocked XMLHttpRequest to:', url);
            return;
        }

        // Optionally modify request headers here
        this.setRequestHeader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0');
        this.setRequestHeader('Accept', 'application/json, text/javascript, */*; q=0.01');
        this.setRequestHeader('Referer', 'https://x.com/');
        this.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        return originalXhrOpen.apply(this, arguments);
    };
})();
