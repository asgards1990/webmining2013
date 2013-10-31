$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre]', function() {
        var genreSelectElement = $(this);
        var keywordSelectElement = $('#' + $(this).attr('id').replace('genre', 'keyword'));
        var keywordWidgetElement = keywordSelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            keywordWidgetElement.yourlabsWidget().autocomplete.data = {
                'genre_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            keywordWidgetElement.yourlabsWidget().autocomplete.data = {}
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(keywordWidgetElement, 'data is', keywordWidgetElement.yourlabsWidget().autocomplete.data)
    })
});