document.addEventListener('DOMContentLoaded', function() {
    console.log("TOC highlight script loaded");
    
    const tocLinks = document.querySelectorAll('.td-toc a');
    console.log("TOC links found:", tocLinks.length);
  
    const sections = document.querySelectorAll('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]');
    console.log("Sections found:", sections.length);
  
    function highlightTOC() {
      console.log("Highlighting TOC");
      let scrollPosition = window.scrollY;
  
      sections.forEach(section => {
        if (section.offsetTop <= scrollPosition + 100) {
          console.log("Active section:", section.id);
          tocLinks.forEach(link => {
            if (link.getAttribute('href') === '#' + section.id) {
              link.classList.add('active');
              console.log("Active link:", link.href);
            } else {
              link.classList.remove('active');
            }
          });
        }
      });
    }
  
    window.addEventListener('scroll', highlightTOC);
    highlightTOC(); // Call once to highlight on page load
  });