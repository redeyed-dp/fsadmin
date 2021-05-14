$(document).ready(function() {

// Сгенерировать пароль
    $('#randompassword').click(function() {
        $.get('/proftpd/randompassword').done(function(response) {
            $('#passwd').val(response);
        }).fail(function() {
            alert("Ошибка! Невозможно подключиться к серверу.");
        });
    });

    $('#homedir-window').on('show.bs.modal', function (event) {
        var modal = $(this);
        modal.find('.modal-title').text('Домашний каталог пользователя ' + $('#userid').val());
        var homedir = $('#homedir').val()
        showDirs(modal, homedir);
    });
});

function showDirs(modal, homedir) {
    $.post('/proftpd/homedir', {
        homedir: homedir
    }).done(function(response) {
        if (!response['exists']) {
            alert ('Каталога ' + homedir + ' не существует');
        }
        var path = response['parent'];
        modal.find('#parent').text(path);
        $('#directories').text('');
        $.each(response['directories'], function(index, value) {
            var dir = document.createElement('li');
            $(dir).addClass('list-group-item').text(value);
            $('#directories').append(dir);
        })
        $('.list-group-item').click(function() {
            $('#directories').find('.active').removeClass('active');
            $(this).addClass('active');
        });
        $('.list-group-item').dblclick(function() {
            if (homedir == '/') {
                homedir = '/' + $(this).text();
            }
            else {
                homedir = homedir + '/' + $(this).text();
            }
            showDirs(modal, homedir);
        });
        $('#dirup').click(function() {
            if (path != '/') {
                var tmp = path.split("/");
                tmp.pop();
                if (tmp.length > 1) {
                    path = tmp.join("/");
                }
                else {
                    path = '/';
                }
                showDirs(modal, path);
            }
        });
        $('#dirsave').click(function() {
            var dir = $('#directories').find('.active').text();
            if (dir != '') {
                path = path + '/' + dir;
            }
            $('#homedir').val(path);
            modal.modal('hide');
        });
    }).fail(function() {
        alert("Ошибка! Невозможно подключиться к серверу.");
    });
}
