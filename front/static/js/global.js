//导航栏鼠标经过事件
$(function () {

});

//获取cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

//获取csrf_token
function getCsrfToken() {
    return getCookie("csrftoken");
}


// 采用正则表达式获取地址栏参数
function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]);  // decodeURI解决中文乱码
    return "";
}

//上传图片选择文件改变后刷新预览图
$("#img").change(function (e) {
    lrz(document.querySelector('input[type=file]').files[0], {
        quality: 0.4 //设置压缩率
    }).then(function (rst) {
        /* 处理成功后执行 */
        //rst.formData.append('base64img', rst.base64); // 添加额外参数
        console.log(rst.file);
        //预览
        let reader = new FileReader();
        reader.readAsDataURL(rst.file);
        reader.onload = function (e) {
            $("#img_show").attr("src", this.result);
        }
    }).catch(function (err) {
        /* 处理失败后执行 */
        console.log("压缩失败");
    }).always(function () {
        /* 必然执行 */
    })
});

//判断是手机端还是电脑端
function browserRedirect(url) {
    var sUserAgent = navigator.userAgent.toLowerCase();
    var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
    var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
    var bIsMidp = sUserAgent.match(/midp/i) == "midp";
    var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
    var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
    var bIsAndroid = sUserAgent.match(/android/i) == "android";
    var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
    var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
    if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
        window.location.href = url;
        return false;
    }
    return true;
}

//paraName 等找参数的名称
/**
 * @return {string}
 */
function getUrlParam(paraName) {
    var url = document.location.toString();
    var arrObj = url.split("?");

    if (arrObj.length > 1) {
        var arrPara = arrObj[1].split("&");
        var arr;
        for (var i = 0; i < arrPara.length; i++) {
            arr = arrPara[i].split("=");
            if (arr != null && arr[0] === paraName) {
                return decodeURI(arr[1]);   // decodeURI解决中文乱码
            }
        }
        return "";
    } else {
        return "";
    }
}

//html剔除富文本标签，留下纯文本
function getSimpleText(html) {
    let reg = new RegExp("<.+?>", "g"); //匹配html标签的正则表达式，"g"是搜索匹配多个符合的内容
    //执行替换成空字符
    return getShortText(html.replace(reg, ''));
}

function getShortText(html) {
    return html.substring(0, 200);
}

//格式化时间
function jsDateDiff(publishTime) {
    var str = publishTime.toString();
    str = str.replace("/-/g", "/");
    var Date1 = new Date(str);
    var publish_time = parseInt(Date1.getTime() / 1000);

    var d_seconds, d_minutes, d_hours, d_days;
    var timeNow = parseInt(new Date().getTime() / 1000);
    var d;
    d = timeNow - publish_time;
    d_days = parseInt(d / 86400);
    d_hours = parseInt(d / 3600);
    d_minutes = parseInt(d / 60);
    d_seconds = parseInt(d);
    if (d_days > 0 && d_days < 4) {
        return d_days + "天前";
    } else if (d_days <= 0 && d_hours > 0) {
        return d_hours + "小时前";
    } else if (d_hours <= 0 && d_minutes > 0) {
        return d_minutes + "分钟前";
    } else if (d_minutes <= 0 && d_seconds > 0) {
        return d_seconds + "秒前";
    } else if (d_days >= 4) {
        var s = new Date(publish_time * 1000);
        return (s.getMonth() + 1) + "月" + s.getDate() + "日" + " " + s.getHours() + ":" + s.getMinutes();
    }
}


/*$('body').click(function (e) {
    var target = $(e.target);
    //如果#overlay或者#btn下面还有子元素，可使用
    //!target.is('#btn *') && !target.is('#overlay *')
    if (!target.is('#btn') && !target.is('#overlay')) {
        if ($('#overlay').is(':visible')) {
            $('#overlay').hide();
        }
    }
});*/

//验证手机号码
function checkPhone(value) {
    let myreg = /^[1][3,4,5,7,8][0-9]{9}$/;
    return myreg.test(value);
}

//sm.ms图床上传图片
// function upload_img_to_sm() {
//     $.ajax({
//         url:
//     })
// }





