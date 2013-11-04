// Lien entre genre1 et keywords

$(document).ready(function() {
	var dict={};
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1SelectElement = $(this);
        var keywordSelectElement = $('#' + $(this).attr('id').replace('genre1', 'keyword'));
        var keywordWidgetElement = keywordSelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            dict['genre1_id'] = value[0];
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        } else {
            // If value is empty, empty autocomplete.data
            dict['genre1_id'] = -2;
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(keywordWidgetElement, 'data is', keywordWidgetElement.yourlabsWidget().autocomplete.data)
    })

// Lien entre genre2 et keywords

    $('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre2SelectElement = $(this);
        var keywordSelectElement = $('#' + $(this).attr('id').replace('genre2', 'keyword'));
        var keywordWidgetElement = keywordSelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            dict['genre2_id'] = value[0];
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        } else {
            // If value is empty, empty autocomplete.data
            dict['genre2_id'] = -2;
            keywordWidgetElement.yourlabsWidget().autocomplete.data = dict;
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(keywordWidgetElement, 'data is', keywordWidgetElement.yourlabsWidget().autocomplete.data)
    })
});

// Lien entre de genre 1 vers genre 2

$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1SelectElement = $(this);
        var genre2SelectElement = $('#' + $(this).attr('id').replace('genre1', 'genre2'));
        var genre2WidgetElement = genre2SelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            genre2WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre1_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            genre2WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre1_id': -2,
            };
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(genre2WidgetElement, 'data is', genre2WidgetElement.yourlabsWidget().autocomplete.data)
    })
});

// Lien entre de genre 2 vers genre 1

$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre2]', function() {
        var genre2SelectElement = $(this);
        var genre1SelectElement = $('#' + $(this).attr('id').replace('genre2', 'genre1'));
        var genre1WidgetElement = genre1SelectElement.parents('.autocomplete-light-widget');

        // When the genre select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            genre1WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre2_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            genre1WidgetElement.yourlabsWidget().autocomplete.data = {
                'genre2_id': -2,
            };
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        console.log($(this), 'changed to', value);
        console.log(genre1WidgetElement, 'data is', genre1WidgetElement.yourlabsWidget().autocomplete.data)
    })
});