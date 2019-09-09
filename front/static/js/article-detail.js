$(function () {
    border_change($(".at-sort-comment-a"), 6);

    $(".article-content img").click(function () { //单击图片放大
        var _this = $(this);//将当前的pimg元素作为_this传入函数
        imgShow("#outerdiv", "#innerdiv", "#bigimg", _this);
    });
});

//验证数据
function check_comment() {
    let commnet_content = vditor.getValue();
    if (commnet_content === "" || commnet_content == null) {
        $("#error-info").text("回复内容不能为空");
        return;
    }
    if (commnet_content.length > 200) {   //文本长度不能超过200
        $("#error-info").text("字数不能超过200");
        return;
    }
    publish_comment();
}

//发表评论
function publish_comment() {
    let article_id = $("#article_id").val();
    let user_id = $("#user_id").val();
    $.ajax({
        type: 'POST',
        url: '/front/publishComment',
        headers: {'X-CSRFToken': getCsrfToken()},
        data: {
            'content': vditor.getValue(),
            'article_id': article_id,
            'user_id': user_id,
        },
        dataType: 'JSON',
        success: function (data) {
            if (data.code === 1) {
                swal({text: data.msg, icon: "success", timer: 1500}).then((value) => {
                    vditor.setValue("");
                    vditor.clearCache();
                    location.reload();
                });
                setTimeout('location.reload()', 1500);
            } else if (data.code === 0) {
                swal({text: data.msg, icon: "error", timer: 1500});
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

//点赞评论
function like_comment(comment_id) {
    /*    if ($("#user_id").val() == null || $("#user_id").val() === "") {    //  判断登陆与否
            sweetAlert("请先登录！");
            return;
        }*/
    $.ajax({
        type: 'POST',
        url: '/front/likeComment',
        headers: {'X-CSRFToken': getCsrfToken()},
        data: {'comment_id': comment_id, 'user_id': $("#user_id").val()},
        dataType: 'JSON',
        success: function (data) {
            if (data.code === 1) {
                location.reload();
            } else if (data.code === 0) {
                swal({text: data.msg, icon: "error", timer: 1500});
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

//回复评论
function reply_comment(obj, comment_id, reply_user_id, article_id) {
    /*    if ($("#user_id").val() == null || $("#user_id").val() === "") {    //  验证登陆
            sweetAlert("请先登录！");
            return;
        }*/
    let text = r_vditor.getValue();
    let reg = /@.*?\:/gi; // 匹配以@开头,:结尾的字符串
    if (text.match(reg) != null) {
        text = text.replace(text.match(reg)[0], "");    //替换字符
    }
    if (text.length > 200 || text.length === 0) {
        swal({text: "字数不能超过200,也不能为空", icon: "error"});
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/front/replyComment',
        headers: {'X-CSRFToken': getCsrfToken()},
        data: {
            'to_comment_id': comment_id,
            'user_id': $("#user_id").val(),
            'reply_user_id': reply_user_id,
            'article_id': article_id,
            'content': text
        },
        dataType: 'JSON',
        success: function (data) {
            console.log(data);
            if (data.code === 1) {
                swal({text: data.msg, icon: "success", timer: 1500}).then((value) => {
                    location.reload();
                });
                setTimeout('location.reload()', 1500);
            } else if (data.code === 0) {
                swal({text: data.msg, icon: "error", timer: 1500});
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

//删除评论
function deleteComment(id) {
    swal("确定要删除吗？", {
        buttons: {
            cancel: "取消",
            catch: {
                text: "确定",
                value: "yes",
            },
        },
    })
        .then((value) => {      //确定按钮事件
            if (value === "yes") {
                $.getJSON(  //发送get类型的ajax请求，返回数据为json格式
                    '/front/deleteComment',    //请求路径
                    {"id": id}, //传递参数
                    function (data) { //接收返回数据
                        if (data.code === 1) { //删除成功
                            swal({text: data.msg, icon: "success", timer: 1500}).then(function () {
                                location.reload();
                            });
                            setTimeout('location.reload()', 1500);
                        } else { //删除失败
                            swal({text: data.msg, icon: "error", timer: 1500});
                        }
                    });
            }
        });
}

let r_vditor;

//显示/隐藏回复框
function show_reply(obj) {
    let display = $(obj).parents('.comment-box').find('.reply-holder').css('display');
    if (display === 'none') {
        $(obj).parents('.comment-box').find('.reply-btn').before(
            '<div id="reply-vditor" class="reply-text-area"></div>'
        );
        r_vditor = init_reply_vditor();
        $(obj).parents('.comment-box').find('.reply-holder').slideDown();
        let user_name = $(obj).parents('.comment-box').find('.user-name').text();
        r_vditor.setValue("@" + user_name + ":");
    } else {
        $(obj).parents('.comment-box').find('.reply-holder').slideUp();
        $(obj).parents('.comment-box').find('#reply-vditor').remove();
    }
}

/*标题栏底部边框长度变化动画*/
function border_change(obj, length) {
    const old_width = $(obj).width();
    const changed_width = old_width + length;
    //鼠标移入底部边框增大
    $(obj).mouseenter(
        function () {
            $(this).animate({width: changed_width});
        });
    //鼠标移出恢复原长度
    $(obj).mouseleave(function () {
        $(this).animate({width: old_width});
    })
}

//初始化vditor
const vditor = new Vditor('vditor', {
    counter: 200,
    height: 300,
    editorName: 'vditor',
    tab: '\t',
    max: 1024,
    toolbar: ['emoji',
        'headings', 'bold', 'italic', 'strike', '|',
        'line', 'quote', 'list', 'ordered-list', 'check', 'code',
        'inline-code', 'undo', 'redo',
        // 'upload',
        'link', 'table', 'record',
        'both', 'preview', 'fullscreen', 'info', 'help', 'br'],
    upload: {
        accept: '.jpg,.png,.gif,.jpeg',
        filename(name) {
            return name.replace(/\?|\\|\/|:|\||<|>|\*|\[|\]|\s+/g, '-')
        },
        //自定义上传图片
        handler(file) {
            /*            if ($("#user_id").val() == null || $("#user_id").val() === "") { //验证登陆
                            sweetAlert("请先登录！");
                            return;
                        }
                        let formData = new FormData(), flag = 1;
                        file.forEach(f => {
                            if (f.size / 1024 > 1536) { //校验图片大小
                                sweetAlert("上传图片大小不能超过1.5M");
                                flag = 0;
                                return;
                            }
                            formData.append('files', f, f.name);
                        });
                        if (flag === 1) {
                            upload_img(formData);
                        }*/
        },
    },
    preview: {
        show: true,
        parse: () => {
            LazyLoadImage()
        },
    },
    hint: {
        emoji: {
            "pray": "🙏",
            "broken_heart": "💔",
            "ok_hand": "👌",
            "smile": "😄",
            "laughing": "😆",
            "smirk": "😏",
            "heart_eyes": "😍",
            "grin": "😁",
            "stuck_out_tongue": "😛",
            "expressionless": "😑",
            "unamused": "😒",
            "sob": "😭",
            "joy": "😂",
            "tired_face": "😫",
            "blush": "😊",
            "cry": "😢",
            "fearful": "😨",
        }
    }
});

//初始化r_vditor
function init_reply_vditor() {
    return new Vditor('reply-vditor', {
        counter: 200,
        height: 200,
        editorName: 'vditor',
        tab: '\t',
        max: 1024,
        toolbar: ['emoji',
            'headings', 'bold', 'italic', 'strike', '|',
            'line', 'quote', 'list', 'ordered-list', 'check', 'code',
            'inline-code', 'undo', 'redo',
            // 'upload',
            'link',
            'both', 'preview', 'fullscreen', 'info', 'help', 'br'],
        upload: {
            accept: '.jpg,.png,.gif,.jpeg',
            filename(name) {
                return name.replace(/\?|\\|\/|:|\||<|>|\*|\[|\]|\s+/g, '-')
            },
            //自定义上传图片
            handler(file) {
                /*                if ($("#user_id").val() == null || $("#user_id").val() === "") { //验证登陆
                                    sweetAlert("请先登录！");
                                    return;
                                }
                                let formData = new FormData(), flag = 1;
                                file.forEach(f => {
                                    if (f.size / 1024 > 1536) { //校验图片大小
                                        sweetAlert("上传图片大小不能超过1.5M");
                                        flag = 0;
                                        return;
                                    }
                                    formData.append('files', f, f.name);
                                });
                                if (flag === 1) {
                                    upload_img(formData);
                                }*/
            },
        },
        preview: {
            show: true,
            mode: 'editor',
            parse: () => {
                LazyLoadImage()
            },
        },
        hint: {
            emoji: {
                "pray": "🙏",
                "broken_heart": "💔",
                "ok_hand": "👌",
                "smile": "😄",
                "laughing": "😆",
                "smirk": "😏",
                "heart_eyes": "😍",
                "grin": "😁",
                "stuck_out_tongue": "😛",
                "expressionless": "😑",
                "unamused": "😒",
                "sob": "😭",
                "joy": "😂",
                "tired_face": "😫",
                "blush": "😊",
                "cry": "😢",
                "fearful": "😨",
            }
        }
    });
}

const LazyLoadImage = () => {
    const loadImg = (it) => {
        const testImage = document.createElement('img');
        testImage.src = it.getAttribute('data-src');
        testImage.addEventListener('load', () => {
            it.src = testImage.src;
            it.style.backgroundImage = 'none';
            it.style.backgroundColor = 'transparent'
        });
        it.removeAttribute('data-src')
    };

    if (!('IntersectionObserver' in window)) {
        document.querySelectorAll('img').forEach((data) => {
            if (data.getAttribute('data-src')) {
                loadImg(data)
            }
        });
        return false
    }

    if (window.imageIntersectionObserver) {
        window.imageIntersectionObserver.disconnect();
        document.querySelectorAll('img').forEach(function (data) {
            window.imageIntersectionObserver.observe(data)
        })
    } else {
        window.imageIntersectionObserver = new IntersectionObserver((entries) => {
            entries.forEach((entrie) => {
                if ((typeof entrie.isIntersecting === 'undefined'
                    ? entrie.intersectionRatio !== 0
                    : entrie.isIntersecting) && entrie.target.getAttribute('data-src')) {
                    loadImg(entrie.target)
                }
            })
        });
        document.querySelectorAll('img').forEach(function (data) {
            window.imageIntersectionObserver.observe(data)
        })
    }
};

//多图片文件上传
function upload_img(formData) {
    $.ajax({
        type: 'POST',
        url: '/vditor/img_upload',
        headers: {'X-CSRFToken': getCsrfCookie("csrftoken")},
        data: formData,
        dataType: 'JSON',
        contentType: false, //不处理数据
        processData: false,
        cache: false,
        success: function (data) {
            console.log(data);
            if (data.code === 1) { // 上传成功，将图片链接写入编辑器
                $.each(data.images, function (i, val) {
                    vditor.focus();
                    let img_url = '\n![](' + val + ')\n';
                    vditor.insertValue(img_url);
                })
            }
            if (data.code === 0) { //上传失败
                alert(data.msg);
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

//获取cookie
function getCsrfCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//点击图片，显示弹窗（放大图片）
function imgShow(outerdiv, innerdiv, bigimg, _this) {
    var src = _this.attr("src");//获取当前点击的img元素中的src属性
    $(bigimg).attr("src", src);//设置#bigimg元素的src属性
    /*获取当前点击图片的真实大小，并显示弹出层及大图*/
    console.log(src);
    $("<img/>").attr("src", src).on('load', function () {
        var windowW = $(window).width();//获取当前窗口宽度
        var windowH = $(window).height();//获取当前窗口高度
        var realWidth = this.width;//获取图片真实宽度
        var realHeight = this.height;//获取图片真实高度
        var imgWidth, imgHeight;
        var scale = 0.88;//缩放尺寸，当图片真实宽度和高度大于窗口宽度和高度时进行缩放
        if (realHeight > windowH * scale) {//判断图片高度
            imgHeight = windowH * scale;//如大于窗口高度，图片高度进行缩放
            imgWidth = imgHeight / realHeight * realWidth;//等比例缩放宽度
            if (imgWidth > windowW * scale) {//如宽度扔大于窗口宽度
                imgWidth = windowW * scale;//再对宽度进行缩放
            }
        } else if (realWidth > windowW * scale) {//如图片高度合适，判断图片宽度
            imgWidth = windowW * scale;//如大于窗口宽度，图片宽度进行缩放
            imgHeight = imgWidth / realWidth * realHeight;//等比例缩放高度
        } else {//如果图片真实高度和宽度都符合要求，高宽不变
            if ((realWidth * 1.2) < windowW && (realHeight * 1.2) < windowH) {
                imgWidth = realWidth * 1.2;
                imgHeight = realHeight * 1.2;
            } else {
                imgWidth = realWidth;
                imgHeight = realHeight;
            }
        }
        $(bigimg).css("width", imgWidth);//以最终的宽度对图片缩放
        var w = (windowW - imgWidth) / 2;//计算图片与窗口左边距
        var h = (windowH - imgHeight) / 2;//计算图片与窗口上边距
        $(innerdiv).css({"top": h, "left": w});//设置#innerdiv的top和left属性
        $(outerdiv).fadeIn("fast");//淡入显示#outerdiv及img
    });

    $(outerdiv).click(function () {//再次点击淡出消失弹出层
        $(this).fadeOut("fast");
    });
}
