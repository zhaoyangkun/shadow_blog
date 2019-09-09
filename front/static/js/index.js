// /*lock = false;
// bgColor = ["rgb(179, 189, 196)", "rgb(180, 183, 166)", "rgb(140, 152, 187)"]; //背景色
// var mySwiper = new Swiper('.swiper-container', {
//     speed: 1500,
//     allowTouchMove: false,//禁止触摸滑动
//     autoplay: {
//         delay: 5000,
//         disableOnInteraction: false,
//     },
//     parallax: true,  //文字位移视差
//     on: {
//         transitionStart: function () {
//             lock = true;//锁住按钮
//             slides = this.slides;
//             imgBox = slides.eq(this.previousIndex).find('.img-box'); //图片包装器
//             imgPrev = slides.eq(this.previousIndex).find('img');  //当前图片
//             imgActive = slides.eq(this.activeIndex).find('img');  //下一张图片
//             derection = this.activeIndex - this.previousIndex;
//             this.$el.css("background-color", bgColor[this.activeIndex]);//背景颜色动画
//             imgBox.transform('matrix(0.6, 0, 0, 0.6, 0, 0)');
//             imgPrev.transition(1500).transform('matrix(1.2, 0, 0, 1.2, 0, 0)');//图片缩放视差
//             this.slides.eq(this.previousIndex).find('h3').transition(1500).css('color', 'rgba(255,255,255,0)');//文字透明动画
//
//             imgPrev.transitionEnd(function () {
//                 imgActive.transition(1500).transform('translate3d(0, 0, 0) matrix(1.2, 0, 0, 1.2, 0, 0)');//图片位移视差
//                 imgPrev.transition(1500).transform('translate3d(' + 60 * derection + '%, 0, 0)  matrix(1.2, 0, 0, 1.2, 0, 0)');
//             });
//         },
//         transitionEnd: function () {
//             this.slides.eq(this.activeIndex).find('.img-box').transform(' matrix(1, 0, 0, 1, 0, 0)');
//             imgActive = this.slides.eq(this.activeIndex).find('img');
//             imgActive.transition(1500).transform(' matrix(1, 0, 0, 1, 0, 0)');
//             this.slides.eq(this.activeIndex).find('h3').transition(1500).css('color', 'rgba(255,255,255,1)');
//
//             imgActive.transitionEnd(function () {
//                 lock = false
//             });
//             //第一个和最后一个，禁止按钮
//             if (this.activeIndex === 0) {
//                 this.$el.find('.button-prev').addClass('disabled');
//             } else {
//                 this.$el.find('.button-prev').removeClass('disabled');
//             }
//
//             if (this.activeIndex === this.slides.length - 1) {
//                 this.$el.find('.button-next').addClass('disabled');
//             } else {
//                 this.$el.find('.button-next').removeClass('disabled');
//             }
//         },
//         init: function () {
//             this.emit('transitionEnd');//在初始化时触发一次transitionEnd事件
//         },
//
//     }
// });
//
// //不使用自带的按钮组件，使用lock控制按钮锁定时间
// mySwiper.$el.find('.button-next').on('click', function () {
//     if (!lock) {
//         mySwiper.slideNext();
//     }
// });
// mySwiper.$el.find('.button-prev').on('click', function () {
//     if (!lock) {
//         mySwiper.slidePrev();
//     }
// });*/

//图片懒加载
$("img").lazyload({
    //placeholder: "", //用图片提前占位
    // placeholder,值为某一图片路径.此图片用来占据将要加载的图片的位置,待图片加载时,占位图则会隐藏
    effect: "fadeIn", // 载入使用何种效果
    // effect(特效),值有show(直接显示),fadeIn(淡入),slideDown(下拉)等,常用fadeIn
    threshold: 100, // 提前开始加载
    // threshold,值为数字,代表页面高度.如设置为200,表示滚动条在离目标位置还有200的高度时就开始加载图片,可以做到不让用户察觉
    //event: 'sporty',  // 事件触发时才加载#}
    // event,值有click(点击),mouseover(鼠标划过),sporty(运动的),foobar(…).可以实现鼠标莫过或点击图片才开始加载,后两个值未测试…
    // container: $("#article-holder"),  // 对某容器中的图片实现效果#}
    // container,值为某容器.lazyload默认在拉动浏览器滚动条时生效,这个参数可以让你在拉动某DIV的滚动条时依次加载其中的图片
    failurelimit: 2 // 图片排序混乱时
    // failurelimit,值为数字.lazyload默认在找到第一张不在可见区域里的图片时则不再继续加载,但当HTML容器混乱的时候可能出现可见区域内图片并没加载出来的情况,failurelimit意在加载N张可见区域外的图片,以避免出现这个问题.
});

/*
$(function () {
    search(1);
});

function search(page) {
    let category = getUrlParam("category");
    $.getJSON(
        '/front/front_article', //请求地址
        {"page": page, "size": 5, 'category': category},  //请求参数
        function (data) {
            initData(data); //渲染数据
            toPage(data); //分页
            //图片懒加载
            $("img.lazy").lazyload({
                //placeholder: "", //用图片提前占位
                // placeholder,值为某一图片路径.此图片用来占据将要加载的图片的位置,待图片加载时,占位图则会隐藏
                effect: "slideDown", // 载入使用何种效果
                // effect(特效),值有show(直接显示),fadeIn(淡入),slideDown(下拉)等,常用fadeIn
                threshold: 100, // 提前开始加载
                // threshold,值为数字,代表页面高度.如设置为200,表示滚动条在离目标位置还有200的高度时就开始加载图片,可以做到不让用户察觉
                //event: 'sporty',  // 事件触发时才加载
                // event,值有click(点击),mouseover(鼠标划过),sporty(运动的),foobar(…).可以实现鼠标莫过或点击图片才开始加载,后两个值未测试…
                //container: $("#article-holder"),  // 对某容器中的图片实现效果#}
                // container,值为某容器.lazyload默认在拉动浏览器滚动条时生效,这个参数可以让你在拉动某DIV的滚动条时依次加载其中的图片
                failurelimit: 1 // 图片排序混乱时
                // failurelimit,值为数字.lazyload默认在找到第一张不在可见区域里的图片时则不再继续加载,但当HTML容器混乱的时候可能出现可见区域内图片并没加载出来的情况,failurelimit意在加载N张可见区域外的图片,以避免出现这个问题.
            }).removeClass("lazy");
        }
    )
}

function initData(data) {
    window.scrollTo(0, 0); //窗口回到顶部
    $(".article-box").remove(); //清空之前数据
    if (data.count === 0) {
        $("#article-holder").append('        <div class="article-box">' +
            '<div class="ab-content" style="height:280px; line-height:280px; text-align:center;">' +
            '<h1>暂无数据</h1>' +
            ' </div>' +
            '</div>');
        return;
    }
    $.each(data.results, function (i, val) {
        let parent_text;
        if (val.category.parent != null) {
            parent_text = '<a href="/front/category/' + val.category.parent.category_name + '">' + val.category.parent.category_name + '</a> <a style="color:#a6a6a6">/</a> ';
        }
        $("#article-holder").append('        <div class="article-box">' +
            '<div class="ab-content">' +
            ' <div class="article-title">' +
            '  <a href="/front/articleDetail/' + val.id + '/">' + val.title + '</a>' +
            ' </div>' +
            '<div class="article-cate">' +
            parent_text +
            '     <a href="/front/label/' + val.category.category_name + '">' + val.category.category_name + '</a>' +
            '   </div>' +
            ' <a href="/front/articleDetail/' + val.id + '/" class="article-img-box">' +
            '  <img class="lazy article-img" data-original="' + val.img + '" alt="" src="/static/img/grey.gif"/>' +
            ' </a>' +
            ' <div class="article-detail-box c-666">' + getSimpleText(val.content) +
            ' </div>' +
            ' <span class="article-tail-box">' +
            '    <i class="fl" style="background-image: url(\"/static/img/read-index.svg\") "></i>\n' +
            '      <span class="read-number c-999 fl">' + val.read_number + '</span>\n' +
            '    <i class="fl" style="background-image: url(\"/static/img/comment-index.svg\") "></i>\n' +
            '      <span class="comment-number c-999 fl">' + val.comment_number + '</span>' +
            ' <span class="article-date c-999">' + jsDateDiff(val.gmt_created) + '</span>' +
            '   <span class="article-author one-line-overflow c-999">' + val.user.user_name + '</span>' +
            ' </span>' +
            ' </div>' +
            '</div>');

    });
}

function toPage(data) {
    new myPagination({
        id: 'pagination',
        curPage: data.current_page, //初始页码
        pageTotal: data.total_pages, //总页数
        pageAmount: 5,  //每页多少条
        dataTotal: data.count, //总共多少条数据
        pageSize: 3, //可选,分页个数
        showPageTotalFlag: true, //是否显示数据统计
        // showSkipInputFlag: true, //是否支持跳转
        getPage: function (page) {
            search(page);
        }
    });
}
*/





