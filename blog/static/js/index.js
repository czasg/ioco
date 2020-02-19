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
    },
    methods: {
        async loading_settings(){
            let settings = await axios.get('./settings.json')
            this.settings = settings.data
            let blog_obj = await axios.get(this.settings.blog_url)
            this.blog_obj = blog_obj.data
            this.all_blogs = this.blog_obj.blogs
            this.$nextTick(() => {
                this.scroll_watching_animation()
            })
        },
        async loading_blog(){
            this.loading_flag = true
            if (this.blog_obj.next_url && this.all_blogs.length < this.settings.blog_total){
                let blog_obj = await axios.get(this.blog_obj.next_url)
                this.blog_obj = blog_obj.data
                this.all_blogs = this.all_blogs.concat(this.blog_obj.blogs)
            }
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
        }
    }
})