# Working-VueJs-Scaffold-app
Test of a scafold app for vue.js with web2py.

This project has the following objectives:
a. Keep simplicity, avoiding installing other software
b. Ease to use, keeping soft learning curve for new comers
c. Seamless Integration with web2py, keeping web2py cybersecurity and access control
d. Minimizing web data exchange, keeping loading times low

Steps to use web2py with Vue.js
1 - Set components with Vue.component() in files *.vue (ex. my-vue-comp.vue)
2 - In *.vue files, Wrap components with <script></script> for syntax highlighting
3 - Place files in a directory inside view folder (ex. a folder named vue)
4 - Include components files in pages (Ex. include 'vue/my-vue-comp.vue') out of script tags
5 - Use root Vue objects on main *.html files
6 - At every root Vue object and component, modify delimiters option (ex: delimiters: ['${', '}'],)
7 - At main *.html, include vue.js and jquery.js
