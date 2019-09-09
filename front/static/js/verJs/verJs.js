window.VerJs = (function () {
    var form;
    var MESSAGE = {
        required: "当前选项不能为空！",
        min: 0,
        max: 0,
        minlength: 0,
        maxlength: 0,
        rule: "",
        equal: "",
        mobile: "请输入有效的手机号码",
        email: "请输入有效的电子邮箱",
        idcard: "请输入有效的身份证号码"
    };
    var change;
    var vers = function (param) {
        if (!ie()) {
            fail(function (d) {
                alert(d)
            }, "不支持的浏览器插件");
            return false
        }
        props;
        style();
        var f = param.form ? param.form : "form";
        form = document.querySelector(f);
        if (param.success) {
            success = param.success
        }
        if (param.fail) {
            fail = param.fail
        }
        change = param.change ? param.change : "default";
        _1(param.data, param.message);
        form.onsubmit = submits;
        form.onreset = rests
    };
    var _1 = function (data, message) {
        if (data) {
            for (var i in data) {
                var names = document.getElementsByName(i);
                [].forEach.call(names, function (item) {
                    for (var j in data[i]) {
                        var messages = message && message[i] && message[i][j] ? message[i][j] : _0.messages[j];
                        if (j != "min" && j != "max" && j != "minlength" && j != "maxlength" && j != "rule" && j != "equal") {
                            item.setAttribute("data-" + j, messages)
                        } else if (j == "rule") {
                            item.setAttribute("data-rule", data[i][j]);
                            item.setAttribute("data-rule-message", messages)
                        } else {
                            item.setAttribute("data-" + j, data[i][j])
                        }
                    }
                })
            }
        }
        for (var i in MESSAGE) {
            var names = form.querySelectorAll("[data-" + i + "]");
            [].forEach.call(names, function (items) {
                var val = items.getAttribute("data-" + i);
                if (val == "true" || val == "false") {
                    items.setAttribute("data-" + i, MESSAGE[i])
                }
                items.onblur = query;
                items.change = query;
                items.onfocus = clear_error;
                if (change == "keyup") {
                    items.onkeyup = query
                }
            })
        }
    };
    var query = function (e) {
        var data = {
            required: required,
            min: minOrMax,
            max: minOrMax,
            minlength: lengths,
            maxlength: lengths,
            rule: rules,
            equal: equal,
            mobile: mobile,
            email: email,
            idcard: IdCard
        };
        var objects = e.target ? e.target : e;
        for (var item in data) {
            if (objects.getAttribute("data-" + item)) {
                data[item]()
            }
        }

        function required() {
            var value = objects.value,
                errorMessage = objects.getAttribute("data-required");
            if (value == '' || value == null) {
                error_tag(errorMessage, objects);
                return false
            }
            return true
        }

        function minOrMax() {
            var value = (objects.value),
                min = parseInt(objects.getAttribute("data-min")),
                max = parseInt(objects.getAttribute("data-max"));
            value = parseInt(value);
            if (value) {
                if (isNaN(value) || min > value) {
                    error_tag("最小值为：" + min, objects);
                    return false
                } else if (!isNaN(max) && max < value) {
                    error_tag("最大值为：" + max, objects);
                    return false
                }
            }
            return true
        }

        function lengths() {
            var value = objects.value.length,
                max = parseInt(objects.getAttribute("data-maxlength")),
                min = parseInt(objects.getAttribute("data-minlength"));
            if (value < min) {
                error_tag("最少输入" + min + "个字符", objects);
                return false
            } else if (value > max) {
                error_tag("最多输入" + max + "个字符", objects);
                return false
            }
            return true
        }

        function rules() {
            var value = objects.value,
                rule = objects.getAttribute("data-rule"),
                errorMessage = objects.getAttribute("data-rule-message");
            if (!errorMessage) errorMessage = "格式错误!";
            rule = new RegExp(rule);
            if (value) {
                if (!rule.test(value)) {
                    error_tag(errorMessage, objects);
                    return false
                }
            }
            return true
        }

        function equal() {
            var value = objects.value,
                equal = document.querySelector(objects.getAttribute("data-equal")).value,
                errorMessage = "两次输入内容不一致";
            if (value != equal) {
                error_tag(errorMessage, objects);
                return false
            }
            return true
        }

        function mobile() {
            var value = objects.value,
                rule_tel = /^(0\d{2,3}\d{7,8}|0\d{2,3}-)\d{7,8}$/,
                rule_phone = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/,
                errorMessage = objects.getAttribute("data-mobile");
            if (value && !rule_phone.test(value) && !rule_tel.test(value)) {
                error_tag(errorMessage, objects);
                return false
            }
            return true
        }

        function email() {
            var value = objects.value,
                rule_email = /^([0-9A-Za-z\-_\.]+)@([0-9a-z]+\.[a-z]{2,3}(\.[a-z]{2})?)$/g,
                errorMessage = objects.getAttribute("data-email");
            if (value && !rule_email.test(value)) {
                error_tag(errorMessage, objects);
                return false
            }
            return true
        }

        function IdCard() {
            var value = objects.value,
                rule_email = /^([1-9]\d{5}[1]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3}[0-9xX]|[1-9]\d{5}\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3})$/,
                errorMessage = objects.getAttribute("data-idcard");
            if (value && !rule_email.test(value)) {
                error_tag(errorMessage, objects);
                return false
            }
            return true
        }
    };
    var error_tag = function (errorMessage, target) {
        clear_error(target);
        var block = target.getAttribute("data-block");
        target.classList.add("ver-error-input");
        var errorTag = document.createElement("span");
        if (!block) {
            var iconCarets = document.createElement("i");
            iconCarets.className = "verJsFont ver-icon-carets ver-error-caret";
            errorTag.appendChild(iconCarets);
            errorTag.className = "ver-errors"
        } else {
            errorTag.className = "ver-errors ver-errorMessageBlock"
        }
        var iconInfo = document.createElement("i");
        iconInfo.className = "verJsFont icon-info-o";
        errorTag.appendChild(iconInfo);
        var span = document.createElement("span");
        span.innerText = errorMessage;
        errorTag.appendChild(span);
        insertAfter(errorTag, target);
        var iconcolor = target.getAttribute("data-icon-color");
        if (iconcolor) {
            var parent = (target.offsetParent);
            var iconcirle = parent.querySelector("iconcirle");
            iconcirle.classList.add("ver-error-inputs")
        }
    };
    var clear_error = function (e) {
        if (e.target) {
            var _0 = e.target
        } else {
            var _0 = e
        }
        var parent = _0.parentElement;
        var errorTag = "";
        if (parent) {
            errorTag = parent.querySelector(".ver-errors");
            if (errorTag) {
                parent.removeChild(errorTag)
            }
            _0.classList.remove("ver-error-input");
            var iconcolor = _0.getAttribute("data-icon-color");
            if (iconcolor) {
                var parent = (_0.offsetParent);
                var iconcirle = parent.querySelector("iconcirle");
                iconcirle.classList.remove("ver-error-inputs")
            }
        }
    };
    var submits = function () {
        verifications();
        var error = form.querySelectorAll(".ver-error-input").length;
        if (error > 0) {
            form.querySelector(".ver-error-input").focus();
            return false
        }
        var forms = form.getAttribute("data-form");
        if (forms === "ajax") {
            sends();
            return false;
        }
        return true;
    };
    var sends = function () {
        var forms = form.getAttribute("data-form");
        var xhr = new XMLHttpRequest();
        // console.log("正在执行的ajax请求路径:" + form.action);
        xhr.open("POST", form.action, true);
        xhr.setRequestHeader("x-requested-with", "XMLHttpRequest");
        var data = new FormData(form);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 203) {
                    return false
                } else if (xhr.status === 200 || xhr.status === 304) {
                    success(xhr.responseText)
                } else {
                    fail(xhr.responseText)
                }
            }
        };
        xhr.send(data)
    };
    var rests = function () {
        form.reset();
        for (var i in MESSAGE) {
            var names = form.querySelectorAll("[data-" + i + "]");
            if (names.length > 0) {
                [].forEach.call(names, function (items) {
                    clear_error(items)
                })
            }
        }
    };
    var verifications = function () {
        for (var i in MESSAGE) {
            var names = form.querySelectorAll("[data-" + i + "]");
            if (names.length > 0) {
                [].forEach.call(names, function (items) {
                    query(items)
                })
            }
        }
    };
    var success = function (data) {
        console.log(data)
    };
    var fail = function (fn, data) {
        console.log(data)
    };
    var getPath = function () {
        var jsPath = document.currentScript ? document.currentScript.src : function () {
            var js = document.scripts,
                last = js.length - 1,
                src;
            for (var i = last; i > 0; i--) {
                if (js[i].readyState === 'interactive') {
                    src = js[i].src;
                    break
                }
            }
            return src || js[last].src
        }();
        return jsPath.substring(0, jsPath.lastIndexOf('/') + 1)
    }();
    var style = function () {
        var css = document.createElement("link"),
            icon = document.createElement("link");
        // css.href = getPath + "need/common.css?v=1.1.0";
        // icon.href = getPath + "need/vericon.css?v=1.1.0";
        css.href = "/static/js/verJs/need/common.css";
        icon.href = "/static/js/verJs/need/vericon.css";
        css.rel = icon.rel = "stylesheet";
        css.type = icon.type = "text/css";
        var link = document.getElementsByTagName("head")[0];
        link.appendChild(css);
        link.appendChild(icon)
    };
    var ie = function () {
        var DEFAULT_VERSION = 8.0;
        var ua = navigator.userAgent.toLowerCase();
        var isIE = ua.indexOf("msie") > -1;
        var safariVersion;
        if (isIE) {
            safariVersion = ua.match(/msie ([\d.]+)/)[1]
        }
        if (safariVersion <= DEFAULT_VERSION) {
            return false
        }
        return true
    };
    var insertAfter = function (item, afters) {
        var parent = afters.parentNode;
        if (parent.lastChild == afters) {
            parent.appendChild(item)
        } else {
            parent.insertBefore(item, afters.nextSibling)
        }
    };
    var props = function () {
        if (!Array.prototype.forEach) {
            Array.prototype.forEach = function (callback, thisArg) {
                var T, k;
                if (this == null) {
                    throw new TypeError(" this is null or not defined")
                }
                var O = Object(this);
                var len = O.length >>> 0;
                if ({}.toString.call(callback) != "[object Function]") {
                    throw new TypeError(callback + " is not a function")
                }
                if (thisArg) {
                    T = thisArg
                }
                k = 0;
                while (k < len) {
                    var kValue;
                    if (k in O) {
                        kValue = O[k];
                        callback.call(T, kValue, k, O)
                    }
                    k++
                }
            }
        }
        if (!("classList" in document.documentElement)) {
            Object.defineProperty(HTMLElement.prototype, 'classList', {
                get: function () {
                    var self = this;

                    function update(fn) {
                        return function (value) {
                            var classes = self.className.split(/\s+/g),
                                index = classes.indexOf(value);
                            fn(classes, index, value);
                            self.className = classes.join(" ")
                        }
                    }

                    return {
                        add: update(function (classes, index, value) {
                            if (!~index) classes.push(value)
                        }),
                        remove: update(function (classes, index) {
                            if (~index) classes.splice(index, 1)
                        }),
                        toggle: update(function (classes, index, value) {
                            if (~index) classes.splice(index, 1);
                            else classes.push(value)
                        }),
                        contains: function (value) {
                            return !!~self.className.split(/\s+/g).indexOf(value)
                        },
                        item: function (i) {
                            return self.className.split(/\s+/g)[i] || null
                        }
                    }
                }
            })
        }
    }();
    return vers
})();