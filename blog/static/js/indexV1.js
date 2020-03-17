// 设置iframe高度自适应
function setIframeHeight(iframe) {
    if (iframe) {
        var iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
        if (iframeWin.document.body) {
            iframe.height = iframeWin.document.documentElement.scrollHeight || iframeWin.document.body.scrollHeight;
        }
    }
};
// 日志模块
class Logger{
    log(obj){
        console.log(obj)
    }
    logs(...args){
        args.forEach((obj) => {
            this.log(obj)
        })
    }
}
var logger = new Logger();
// Vue实例
var app = new Vue({
    el: '#app',
    created(){
        this.$nextTick(() => {
            this.loading_settings()
            addEventListener('scroll', this.scroll_watching)
        })
    },
    mounted(){
        this.$refs.search_box.onfocus = () => { this.search_flag = true; }
        this.$refs.search_box.onblur = () => {
            if (!this.input_content){
                this.search_flag = false;
            }
        }
    },
    data:{
        settings: {},  // 全局配置数据
        page_count: 1,
        blog_url: '',  // 绑定详情页

        search_flag: false,  // 搜索过滤
        loading_flag: true,  // 加载动画
        blog_detail: false,  // 博客详情页 true => iframe
        label_flag: false,  // 是否由标签加载数据

        input_content: '',  // 绑定搜索框文本内容
        index_blog: [],
        blog_obj: {},

        label_blog: [],
        label_obj: {},
        label_blog_total: 0,
        label_page_total: 0,
    },
    updated(){
        this.show_all_blog()
    },
    methods: {
        searching: function(blogs, searching_key){
            return blogs.filter(blog => {
                if (blog.blog_title.includes(searching_key)){
                    return true
                }
            })
        },
        async loading_settings(){
            let settings = await axios.get('./settings.json')
            this.settings = settings.data
            let blog_obj = await axios.get(this.settings.blog_url)
            this.blog_obj = blog_obj.data
            this.index_blog = this.blog_obj.blogs
            this.anime_func_all()
            this.loading_flag = false
            this.show_all_blog()
        },
        async loading_blog(){
            if (this.blog_detail) return
            if (this.loading_flag) return
            this.loading_flag = true
            setTimeout(()=>{
                if (this.label_flag){
                    this._loading_blog(this.label_obj, this.label_blog, this.label_blog_total)
                } else {
                    this._loading_blog(this.blog_obj, this.index_blog, this.settings.blog_total)
                }
                this.loading_flag = false
            }, 1000)
        },
        async _loading_blog(blog_obj, all_blog, blog_total){
            if (blog_obj.next_url && all_blog.length < blog_total){
                let blog_obj_temp = await axios.get(blog_obj.next_url)
                if (this.label_flag) {
                    this.label_obj = blog_obj_temp.data
                    this.label_blog = this.label_blog.concat(this.label_obj.blogs)
                }else{
                    this.blog_obj = blog_obj_temp.data
                    this.index_blog = this.index_blog.concat(this.blog_obj.blogs)
                }
                this.page_count += 1
                this.anime_func_all()
            }
        },
        scroll_watching: function(){
            this.scroll_watching_loading()
            this.scroll_watching_animation()
        },
        scroll_watching_loading: function(){
            var
                win = $(window),
                doc = $(document),
                scrollTop = win.scrollTop(),
                scrollHeight = doc.height(),
                windowHeight = win.height();
            if(scrollTop + windowHeight + 1 > scrollHeight){
        　　　　this.loading_blog();
        　　}
        },
        scroll_watching_animation: function(){
            let top = pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
	  		let vh = document.documentElement.clientHeight
	  		let dom = document.querySelectorAll(".blog-box")
	  		dom.forEach(v => {
	  		    if(top + vh > v.offsetTop){
                    v.style.opacity = 1
                    v.style.top = 0
	  		    } else{
	  		        v.style.opacity = 0
                    v.style.top = '100px'
	  		    }
	  		})
        },
        blog_detail_func: function(url){
            this.blog_url = url
            this.blog_detail = true
            this.loading_flag = true
            this.$nextTick(() => {
                iframe = document.getElementById('blog-iframe')
                iframe.onload = () => {
                    this.loading_flag = false
                    setIframeHeight(iframe)
                }
            })
        },
        show_all_blog:function(){
            this.$nextTick(()=>{
                this.scroll_watching_animation()
            })
        },
        anime_func_all: function(){
            if (this.label_flag) {
                this._anime_func_all(this.label_blog, this.label_blog_total, this.label_page_total)
            } else {
                this._anime_func_all(this.index_blog, this.settings.blog_total, this.settings.blog_total_page)
            }
        },
        _anime_func_all(all_blog, blog_total, pages_total){
            this.anime_func('#blog_count_svg', '#blog_count', all_blog.length, blog_total)
            this.anime_func('#blog_page_count_svg', '#blog_page_count', this.page_count, pages_total)
        },
        anime_func: function(h3id, blogId, num, all_num){
            var
                h3 = document.querySelector(h3id),
                obj = {count: 0};
            anime({
                targets: `${blogId} .path-loop`,
                strokeDashoffset: function(el) {
                    var svgLength = anime.setDashoffset(el);
                    return [svgLength, svgLength*(1-num/all_num)];
                },
                easing: 'linear',
                duration: 2000,
                update: function(){}
            });
            anime({
                targets: obj,
                count: num,
                easing: 'linear',
                duration: 2000,
                round: 1,
                update: function(){
                    h3.innerText = `${obj.count}/${all_num}`
                }
            });
        },
        async loading_label(label){
            this.loading_flag = true
            this.label_flag = true
            this.blog_detail = false
            let blog_obj = await axios.get(label.url)
            this.label_obj = blog_obj.data
            this.label_blog = this.label_obj.blogs
            this.page_count = 1
            this.label_blog_total = label.total
            this.label_page_total = label.total_page
            this.anime_func_all()
            this.loading_flag = false
        },
        choose_label_blog: function(){
            if (this.label_flag){
                return this.label_blog
            } else {
                return this.index_blog
            }
        }
    }
})

