$(document).ready(function () {
    $('#actors input, #genres input').each(function () {
        var self = $(this),
                label = self.next(),
                label_text = label.text();

        label.remove();
        self.iCheck({
            checkboxClass: 'icheckbox_line-red',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        });
    });
});