var IMAGE_URL = '';
// <script src="{% static 'js/jquery.min.js' %}"/>

var myalert = {
    alertInfoWithTitle: function (message, title) {
        alert(title + ': ' + message);
    }
};

// function Check() {
//     this.DOWNLOAD_URL = '';
// }
//
// $(document).ready(function () {
//     var check = new Check();
//     check.run();
// });
// Check.prototype.listenCheckEvent = function () {
//     const changeBtn = $('#check-btn');
//     changeBtn.click(function (event) {
//         event.preventDefault();
//         const input_content = $('#input-text').val();
//         const file_input = $('#file-input').val();
//         $.ajax({
//             'type': 'POST',
//             'url': ['/check_content/','/text-analysis/'],
//             'data': {
//                 input_content,
//                 file_input
//             },
//             'success': function (result) {
//                 if (result['code'] === 200) {
//                     var pred_name = result['data']['pred_name'];
//                     myalert.alertInfoWithTitle(pred_name, '检测成功!');
//                 } else {
//                     myalert.alertInfoWithTitle(result['message'], '错误信息')
//                 }
//             }
//         })
//     })
//
// };// check.js
// document.getElementById('upload-btn').addEventListener('click', handleUpload);
//
// function handleUpload() {
//   const fileInput = document.getElementById('file-input');
//   const file = fileInput.files[0];
//
//   if (!file) {
//     alert('请先选择文件');
//     return;
//   }
//   // 文件类型校验
//   const allowedTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
//   if (!allowedTypes.includes(file.type)) {
//     alert('仅支持 CSV 和 XLSX 格式');
//     return;
//   }
//    const formData = new FormData();
//   formData.append('file', file);
//   formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
//
//   // 显示上传状态
//   const statusEl = document.getElementById('upload-status');
//   statusEl.textContent = '上传中...';
// // 替换 fetch 为 XMLHttpRequest 以支持进度监控
// const xhr = new XMLHttpRequest();
// xhr.open('POST', '/api/upload/');
//
// xhr.upload.addEventListener('progress', (e) => {
//   if (e.lengthComputable) {
//     const percent = Math.round((e.loaded / e.total) * 100);
//     statusEl.textContent = `上传进度：${percent}%`;
//   }
// });
//
// xhr.onload = function() {
//   if (xhr.status === 200) {
//     statusEl.textContent = '上传成功';
//   }
// };
//
// xhr.send(formData);
// }
//
//
//
// Check.prototype.listenUploadEvent = function () {
// $(document).on('click', '#upload-btn', function (event) {
//     event.preventDefault();
//     console.log('上传按钮被点击'); // 添加这行代码
//     var file = $('#file-input')[0].files[0];
//     if (!file) {
//         myalert.alertInfoWithTitle('请选择文件', '提示');
//         return;
//     }
// var allowedExtensions = ['xlsx', 'csv'];
// var fileExtension = file.name.split('.').pop().toLowerCase();
//
// if (!allowedExtensions.includes(fileExtension)) {
//     myalert.alertInfoWithTitle('请选择正确的文件格式（.xlsx 或 .csv）', '提示');
//     return;
// }
//     var formData = new FormData();
//     formData.append('file', file);
//
//     var uploadStatus = $('#upload-status');
//     uploadStatus.text('上传中...');
//     $('#download-btn').hide();
//
//     $.ajax({
//         'type': 'POST',
//         'url': '/upload-file-analysis/',
//         'data': formData,
//         'processData': false,
//         'contentType': false,
//         'success': function (result) {
//              console.log('请求成功:', result); // 添加这行代码
//             uploadStatus.text('');
//             if (result['code'] === 200) {
//                 myalert.alertInfoWithTitle('文件上传成功，可以下载检测结果了', '提示');
//                 this.DOWNLOAD_URL = result['data']['download_url'];
//                 $('#download-btn').show();
//             } else {
//                 myalert.alertInfoWithTitle(result['message'], '错误信息');
//             }
//         }.bind(this),
//         'error': function () {
//             uploadStatus.text('');
//             myalert.alertInfoWithTitle('文件上传失败', '错误信息');
//         }
//     });
// }.bind(this));
// };
//
// Check.prototype.listenDownloadEvent = function () {
//     $('#download-btn').click(function () {
//         if (this.DOWNLOAD_URL) {
//             window.location.href = this.DOWNLOAD_URL;
//         } else {
//             console.log('检测结果不存在');
//             myalert.alertInfoWithTitle('检测结果不存在', '提示');
//         }
//     }.bind(this));
// };
//
//
//
// Check.prototype.run = function () {
//     var self = this;
//      self.listenCheckEvent();
//     self.listenUploadEvent();
//     self.listenDownloadEvent();
// };
//
//
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//
// $.ajaxSetup({
//     beforeSend: function (xhr, settings) {
//         if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//         }
//     }
// });
//
// $(function () {
//     var check = new Check();
//     check.run();
// });
//
// // $(document).ready(function () {
// //     $('#upload-btn').click(function () {
// //         console.log('上传按钮被点击');
// //     });
// // });
var IMAGE_URL = '';
var myalert = {
    alertInfoWithTitle: function (message, title) {
        alert(title + ': ' + message);
    }
};

function Check() {
    this.DOWNLOAD_URL = '';
}

Check.prototype.listenUploadEvent = function () {
    $(document).on('click', '#upload-btn', function (event) {
        event.preventDefault();
        console.log('上传按钮被点击'); // 确保这行代码被执行
        var file = $('#file-input')[0].files[0];
        if (!file) {
            myalert.alertInfoWithTitle('请选择文件', '提示');
            return;
        }

        var allowedExtensions = ['xlsx', 'csv'];
        var fileExtension = file.name.split('.').pop().toLowerCase();

        if (!allowedExtensions.includes(fileExtension)) {
            myalert.alertInfoWithTitle('请选择正确的文件格式（.xlsx 或 .csv）', '提示');
            return;
        }

        var formData = new FormData();
        formData.append('file', file);

        var uploadStatus = $('#upload-status');
        uploadStatus.text('上传中...');
        $('#download-btn').hide();

        $.ajax({
            'type': 'POST',
            'url': '/upload-file-analysis/', // 确保与后端接口一致
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                console.log('请求成功:', result); // 确保这行代码被执行
                if (result['code'] === 200) {
                    if (result['data'] && result['data']['download_url']) {
                        myalert.alertInfoWithTitle('文件上传成功，可以下载检测结果了', '提示');
                        this.DOWNLOAD_URL = result['data']['download_url'];
                        $('#download-btn').show();
                    } else {
                        console.error('Invalid response format:', result);
                        myalert.alertInfoWithTitle('后端返回的数据格式不正确', '错误信息');
                    }
                } else {
                    myalert.alertInfoWithTitle(result['message'], '错误信息');
                }
            }.bind(this),
            'error': function () {
                uploadStatus.text('');
                myalert.alertInfoWithTitle('文件上传失败', '错误信息');
            }
        });
    }.bind(this));
};

Check.prototype.listenDownloadEvent = function () {
    $('#download-btn').click(function () {
        if (this.DOWNLOAD_URL) {
            window.location.href = this.DOWNLOAD_URL;
        } else {
            console.log('检测结果不存在');
            myalert.alertInfoWithTitle('检测结果不存在', '提示');
        }
    }.bind(this));
};

Check.prototype.run = function () {
    var self = this;
    self.listenCheckEvent();
    self.listenUploadEvent();
    self.listenDownloadEvent();
};

$(document).ready(function () {
    var check = new Check();
    check.run();
});
$(document).ready(function () {
    var check = new Check();
    check.run();
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});