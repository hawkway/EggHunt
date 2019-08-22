// ==UserScript==
// @name        eggs
// @namespace   PBIAL
// @description turn off autoplay
// @include     
// @version     1
// @grant       none
// ==/UserScript==

var jQueryLoadMilliseconds = 500;

// create new script element
var jq = document.createElement('script');
// add jquery to contents of new element
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js";
// insert jquery into head element to make life easier
document.getElementsByTagName('head')[0].appendChild(jq);

function main()
{
    // for each link
    $('a').each(function()
    {
        // if link contains egg text
        if ($(this).is('[href*="tool=w00t"]'))
        {
            // load window to egg url
            var url = $(this).attr('href');
            window.location.href = url;
        } // if
    }); // foreach
} // main

// start here
setTimeout(main, jQueryLoadMilliseconds);
