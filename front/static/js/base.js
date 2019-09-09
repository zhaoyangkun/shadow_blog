$(function () {

    //搜索框回车事件
    $('#search-input').bind('keypress', function (event) {
        if (event.keyCode === 13) {
            search_by_key();
        }
    });

    //首页搜索栏聚焦事件
    $("#search-input").focus(function () {
        $(".search-s").addClass("search-on");  //改变边框和icon的颜色
        $(".search-icon").addClass("icon-on");
    });

    //首页搜索栏失去焦点事件
    $("#search-input").blur(function () {
        $(".search-s").removeClass("search-on"); //恢复边框和icon的颜色
        $(".search-icon").removeClass("icon-on");
    });

    //首页搜索栏聚焦事件
    $("#search-input-m").focus(function () {
        $(".search-s").addClass("search-on");  //改变边框和icon的颜色
        $(".search-icon").addClass("icon-on");
    });

    //首页搜索栏失去焦点事件
    $("#search-input-m").blur(function () {
        $(".search-s").removeClass("search-on"); //恢复边框和icon的颜色
        $(".search-icon").removeClass("icon-on");
    });

    $(".a-login").hover(
        function () {   //鼠标移入显示下拉栏
            $(this).next(".nav-ul-m").stop(true, false).toggle();
            {
                $(this).addClass('nb-a-hover');
            }
        }, function () {    //鼠标移出隐藏下拉栏
            $(this).next(".nav-ul-m").stop(true, false).toggle();
            {
                $(this).removeClass('nb-a-hover');
            }
        }
    );

    $(".nav-li-m").hover(
        function () {   //鼠标移入下拉栏显示下拉栏，并改变下拉栏背景色和字体色
            $(this).parent(".nav-ul-m").stop(true, false).toggle();
            {
                $(this).parent(".nav-ul").prev('.nb-a').addClass('nb-a-hover');
            }
            {
                $(this).addClass('li-hover');
            }
        }, function () {    //鼠标移出下拉栏隐藏下拉栏
            $(this).parent(".nav-ul-m").stop(true, false).toggle();
            {
                $(this).parent(".nav-ul").prev('.nb-a').removeClass('nb-a-hover');
            }
            {
                $(this).removeClass('li-hover');
            }
        }
    );

    //隐藏/显示移动端侧边栏
    $("#mobile_cate").click(function (event) {
        $("#nav-m-list").delay(100).animate({right: '0'}, 500);
        $(document).one("click", function () { //对document绑定一个影藏Div方法
            $("#nav-m-list").delay(100).animate({right: '-250px'}, 500);
        });
        event.stopPropagation(); //阻止事件向上冒泡
        $("#nav-m-list").click(function (event) {
            event.stopPropagation(); //阻止事件向上冒泡
        });
    });

    $("#cancel").click(function () {
        $("#nav-m-list").delay(100).animate({right: '-250px'}, 500);
    })
});

//返回顶部
const top_to = new Top({dImg: "/static/img/up-d.png", hImg: "/static/img/up-d.png"});

//注销
function logout() {
    $.ajax({
        url: "/admin/login",
        type: 'DELETE',
        headers: {'X-CSRFToken': getCsrfToken()},
        success: function (data) {
            if (data.code === 1) {
                window.location.href = '/front/loginDis';
            }
        },
        error: function (data) {
            console.log(data);
        }
    });

}

//关键字搜索
function search_by_key() {
    if ($("#search-input").val() === "" || $("#search-input").val() == null) {
        sweetAlert({text: '请输入关键词！', timer: 1500});
        return;
    }
    window.location.href = '/front/search/' + $("#search-input").val() + '/';
}

function m_search() {
    if ($("#search-input-m").val() === "" || $("#search-input-m").val() == null) {
        sweetAlert({text: '请输入关键词！', timer: 1500});
        return;
    }
    window.location.href = '/front/search/' + $("#search-input-m").val() + '/';
}

$(".nb-a").hover(
    function () {   //鼠标移入显示下拉栏
        $(this).next(".nav-ul").stop(true, false).show();
        $(this).addClass('nb-a-hover');
    }, function () {    //鼠标移出隐藏下拉栏
        $(this).next(".nav-ul").stop(true, false).hide();
        $(this).removeClass('nb-a-hover');
    }
);

$(".nav-li").hover(
    function () {   //鼠标移入下拉栏显示下拉栏，并改变下拉栏背景色和字体色
        $(this).parent(".nav-ul").stop(true, false).show();
        $(this).parent(".nav-ul").prev('.nb-a').addClass('nb-a-hover');
        $(this).addClass('li-hover');
    }, function () {    //鼠标移出下拉栏隐藏下拉栏
        $(this).parent(".nav-ul").stop(true, false).hide();
        $(this).parent(".nav-ul").prev('.nb-a').removeClass('nb-a-hover');
        $(this).removeClass('li-hover');
    }
);

