// 滑动验证码
var handlerPopup = function (captchaObj) {
    // 成功的回调
    captchaObj.onSuccess(function () {
        var validate = captchaObj.getValidate();
        $.ajax({
            url: "/login/", // 进行二次验证
            type: "post",
            dataType: "json",
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
                geetest_challenge: validate.geetest_challenge,
                geetest_validate: validate.geetest_validate,
                geetest_seccode: validate.geetest_seccode
            },
            success: function (data) {
                if (data["user"]) {
                    location.href = "/index/"
                }
                else {
                    $("#error").html(data["msg"]).css({"color": "red"})
                }
            }
        });
    });
    $(".login-btn").click(function () {
        captchaObj.show();
    });
    // 将验证码加到id为captcha的元素里
    captchaObj.appendTo("#popup-captcha");
    // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
};
// 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
$.ajax({
    url: "/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
    type: "get",
    dataType: "json",
    success: function (data) {
        // 使用initGeetest接口
        // 参数1：配置参数
        // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
        initGeetest({
            gt: data.gt,
            challenge: data.challenge,
            product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
            offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
            // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
        }, handlerPopup);
    }
});

// input标签内容改变事件，即头像上传
$("#avatar").change(function () {
    var file = $(this)[0].files[0];  // 获取图片路径
    var reader = new FileReader();  // 文本阅读器
    reader.readAsDataURL(file);  // 读取文件的路径
    reader.onload = function () {
        $("#avatar_img").attr("src", reader.result)  // 将图片的路径写入img标签的src中
    }
});

// 注册用户
$(".reg-btn").click(function () {
    var formdata = new FormData();
    var request_list = $("#form").serializeArray();  // 包含form表单中所有标签的name和value
    $.each(request_list, function (index, data) {
        formdata.append(data.name, data.value)
        /*
       相当于：
           formdata.append("username",$("#id_username").val());
           formdata.append("password",$("#id_password").val());
           formdata.append("re_password",$("#id_re_password").val());
              formdata.append("email",$("#id_email").val());
       */
    });
    formdata.append("avatar", $("#avatar")[0].files[0]);
    $.ajax({
        url: "/register/",
        type: "POST",
        contentType: false,  // 必加参数
        processData: false,  // 必加参数
        data: formdata,
        success: function (data) {
            console.log(data);
            $("span.error").html("");  // 移除上一次的错误信息
            $(".has-error").removeClass("has-error");  // 移除上一次错误信息框样式
            if (data.user) {
                location.href = "/login/"
            }
            else {
                var error_list = data.msg;
                $.each(error_list, function (field, error) {
                    if (field == "__all__") {
                        // 对全局钩子的单独处理
                        $("#id_re_password").next().html(error[0]).parent().addClass("has-error")
                    }
                    $("#id_" + field).next().html(error[0]);  // 找寻对应id的input标签后面的span标签，将错误信息写入
                    $("#id_" + field).parent().addClass("has-error");  // 给含有错误信息的input标签添加css样式
                })
            }
        }
    })
});


// 用户更换头像
$("#change_avatar").click(function () {
    var formdata = new FormData();
    formdata.append("avatar", $("#avatar")[0].files[0]);
    console.log(formdata.get("avatar"));
    $.ajax({
        url: "/change_avatar/",
        type: "POST",
        contentType: false,  // 必加参数
        processData: false,  // 必加参数
        data: formdata,
        success:function () {
            location.href = "/back_stage";
        }
    })
});