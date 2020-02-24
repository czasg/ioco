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
var logger = new Logger()
function setIframeHeight(iframe) {
    if (iframe) {
        var iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
        if (iframeWin.document.body) {
            iframe.height = iframeWin.document.documentElement.scrollHeight || iframeWin.document.body.scrollHeight;
        }
    }
};
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
            if (!this.search_content){
                this.search_flag = false;
            }
        }
    },
    data:{
        settings: {},
        search_flag: false,
        search_content: '',
        all_blogs: [],
        blog_obj: {},
        loading_flag: true,
        blog_page: false,
        blog_url: '',
        page_count: 1,
        label_blogs: [],
        label_obj: {},
        label_blog_total: 0,
        label_page_total: 0,
        label_flag: false,
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
            this.all_blogs = this.blog_obj.blogs
            this.anime_func_all()
            this.$nextTick(() => {
                this.loading_flag = false
                this.scroll_watching_animation()
            })
        },
        async loading_blog(){
            if (this.blog_page) return
            if (this.loading_flag) return
            this.loading_flag = true

            if (this.label_flag){
                var blog_obj = this.label_obj,
                    all_blogs = this.label_blogs,
                    blog_total = blog_obj.total;
            } else {
                var blog_obj = this.blog_obj,
                    all_blogs = this.all_blogs,
                    blog_total = this.settings.blog_total;
            }

            if (blog_obj.next_url && all_blogs.length < blog_total){
                let blog_obj_temp = await axios.get(blog_obj.next_url)

                if (this.label_flag) {
                    this.label_obj = blog_obj_temp.data
                    this.label_blogs = this.label_blogs.concat(this.label_obj.blogs)
                }else{
                    this.blog_obj = blog_obj_temp.data
                    this.all_blogs = this.all_blogs.concat(this.blog_obj.blogs)
                }
                this.page_count += 1
                this.anime_func_all()
            }
//            if (this.blog_obj.next_url && this.all_blogs.length < this.settings.blog_total){
//                let blog_obj = await axios.get(this.blog_obj.next_url)
//                this.blog_obj = blog_obj.data
//                this.all_blogs = this.all_blogs.concat(this.blog_obj.blogs)
//                this.page_count += 1
//                this.anime_func_all()
//            }
            this.loading_flag = false
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
	  		let dom = document.querySelectorAll(".blog-row")
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
        blog_detail: function(url){
            this.blog_url = url
            this.blog_page = true
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
            this.blog_page = false;
            this.$nextTick(()=>{
                this.scroll_watching_animation()
            })
        },
        show_labels_blog: function(){
            this.label_flag = false;
            this.blog_page = false;
            this.$nextTick(()=>{
                this.scroll_watching_animation()
            })
        },
        anime_func_all: function(){
            if (this.label_flag) {
                blogs = this.label_blogs
                blogs_total = this.label_blog_total
                pages_total = this.label_page_total
            } else {
                blogs = this.all_blogs
                blogs_total = this.settings.blog_total
                pages_total = this.settings.blog_total_page
            }
            var num = 0
            blogs.forEach((data) => {
                num += data.length
            })
            this.anime_func('#blog_count_svg', '#blog_count', num, blogs_total)
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
//            this.blog_page = true
            let blog_obj = await axios.get(label.url)
            this.label_obj = blog_obj.data
            this.label_blogs = this.label_obj.blogs
            this.page_count = 1
            this.label_blog_total = label.total
            this.label_page_total = label.total_page
            this.anime_func_all()
            this.loading_flag = false
        },
        choose_label_blog: function(){
            if (this.label_flag){
                return this.label_blogs
            } else {
                return this.all_blogs
            }
        }
    }
})

