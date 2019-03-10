<!-- 
/* Tutorial for Vue with Web2py 
1 - Set components with syntax for single page declaration in files *.vue (ex. my-vue-comp.vue)
2 - In *.vue files, Wrap components with <script></script> for syntax highlighting
3 - Place files in a directory inside view folder (ex. a folder named vue)
4 - Include components files in pages (Ex. include 'vue/my-vue-comp.vue') out of script tags
5 - Use root Vue objects on main *.html files
6 - At every root Vue object and component, modify delimiters option (ex: delimiters: ['${', '}'],)
7 - At main *.html, include vue.js and jquery.js
8 - Code mix: disable code validation 
  (Project...Codemix/validation and build/enable codemix project validation = false)

 */
-->
<script>

Vue.component('source-file-line', {
    delimiters: ['${', '}'],
    data : function (){
        return {
            isSelected: null != this.lineProp.code_text ? this.selected : true,
            //lineIndex: this.lineProp.vid,
            numberOfSpaces: 1,
            //rawcode_Text: this.lineProp.code_text,
            compiledLanguages: ''
        }
    },
    props : {
        selected: {
            type: Boolean,
            default: false
        },
        lineProp: Object,
        language:{
          type: [String, Array],
          default: 'js'
        }
    },
    template:  '<li v-if="isSelected">\
                    <input \
                        :id="lineId" \
                        type="text" \
                        placeholder="Your code here..."\
                        @blur="unselect" \
                        v-model=lineProp.code_text \
                        class="source-line-writing"></input>\
                    </li>\
                <li v-else ><button \
                        class="add-button-class"\
                        @click="$emit(\'insertline\')"\
                        ><slot\
                            name="add-button"\
                            >Add</slot></button><pre\
                        @click="selectLine"\
                        >${lineProp.vid} ${indentLine(numberOfSpaces)}<code\
                            :id="lineId"\
                            :class="languages"\
                            v-html="highlightedLine"\
                        ></code></pre><button\
                        class="remove-button-class"\
                        @click="$emit(\'removeline\')"\
                        ><slot \
                            name="remove-button"\
                            >Remove</slot></button>\
                </li>',
    methods: {
        selectLine: function(event){
            this.isSelected = true;
            Vue.nextTick(this.getFocus);
        },
        unselect: function(){
            if(this.lineProp.code_text.length>0){
                this.isSelected = false;
            }else{

            }
            Vue.set(this.lineProp, 'saved', false);
            this.$emit('changeline');
            },
            
        indentLine: function(){
            return new Array(this.numberOfSpaces).join(' ');
            },
        /* This function may be called after a text change event. However, we need to wait Vue update
        the element before making the highlighting. This function needs the 'language-*' class on code
        element to work. It was abandoned because the elements lost its dynamic link.
        Anyway, if anyone wants to try, remeber to use nextTick function to wait screen update before
        highlighting:*/
        //Vue.nextTick(this.highlightSyntax);
        highlightSyntax: function (){
            Prism.highlightElement(document.getElementById(this.lineId));
            },
        getFocus: function (){
            $("#" + this.lineId).focus();
            },
        },
    computed: {
        lineId: function(){return 'source-file-line-' + this.lineProp.vid;},
        highlightedLine: function (){
            return Prism.highlight(this.lineProp.code_text, Prism.languages.markup);
        },
        languages: function (){
            var strsum = '';
            if(typeof this.language === 'string'){
                strsum = 'language-' + this.language;
            }else{
                this.language.forEach(function(element){
                    strsum += ' language-' + element;
                    });
                }
            return strsum
            },
        }
    })//component
</script>