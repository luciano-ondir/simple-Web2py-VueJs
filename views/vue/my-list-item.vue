<!-- 
/* Tutorial for Vue with Web2py 
1 - Set components with syntax for single page declaration in files *.vue (ex. my-vue-comp.vue)
2 - In *.vue files, Wrap components with <script></script> for syntax highlighting
3 - Place files in a directory inside view folder (ex. a folder named vue)
4 - Include components files in pages (Ex. include 'vue/my-vue-comp.vue') out of script tags
5 - Use root Vue objects on main *.html files
6 - At every root Vue object and component, modify delimiters option (ex: delimiters: ['${', '}'],)
7 - At main *.html, include vue.js and jquery.js


*/
-->
<script>

Vue.component('my-list-item', {
    delimiters: ['${', '}'],
    data : function (){
        return {
            dataSelected: this.selected,
            currentClass: 'non-selected'}
        },
    props : {
        linename: {type: String,
            default: 'My line default name!'}, 
        recordIndex: {
            type: [Number, String],
            default: 0
        },
        selected: {
            type: Boolean,
            default: false
        },
        checkCallback: Function},
    template: '<li @click="selectLine" \
                :class="{selected: dataSelected, strong: dataSelected}"> \
                ${recordIndex} - ${ linename }\
                </li>',
    methods: {
        selectLine: function(event){
            
            if (true == this.dataSelected){
                this.checkCallback(null, null);
                }
            else{
                this.checkCallback(this.unselect, this.recordIndex);
                this.dataSelected = true;
                }
            },
        unselect: function(){
            this.dataSelected = false;
            },
        }
    })
</script>