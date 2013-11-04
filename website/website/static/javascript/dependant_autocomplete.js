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






/*function ajoutKeywordSuggest(keyword) {

var newKeyword = document.createElement('div');
newKeyword.className="keyword";


var newName = document.createElement('span');
newName.className="name";


newName.appendChild(document.createTextNode(keyword));



var newDelete = document.createElement('span');                               
newDelete.className="delete";


var newImg1 = document.createElement('img');
newImg1.className="add1";
newImg1.src="img/DeleteGrey.jpg" 


var newImg2 = document.createElement('img');
newImg2.className="add2"; 
newImg2.src="img/DeleteRed.png" ;


newKeyword.appendChild(newName);
newKeyword.appendChild(newDelete);
newDelete.appendChild(newImg1);
newDelete.appendChild(newImg2);

document.getElementById("keywordSuggest").appendChild(newKeyword);

return newImg1;
return newImg1;
};*/





$(document).ready(function() {
    $('body').on('change', '.autocomplete-light-widget select[name$=genre1]', function() {
        var genre1 = $('#id_genre1');
        var genre2 = $('#id_genre2');
        var id1 = genre1.val();
        var id2 = genre2.val();
        urlSubmit = 'http://Senellart.com:8080/suggest/';

        if (id1) {
            var value1 = $('#id_genre1-deck').clone().children().children().remove().end().text();
            alert (value1);
        
            if (id2) {
                var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
                alert (value2);
                };
           /* else {
                $.post({
                    url: urlSubmit,
                    msg="json.request"+JSON.stringify(???: 'value1', )
                    success:function callback(response){
                        if (response.success) {
                            for (k=0;k<10;k++) {
                            ajoutKeywordSuggest(response.resuslts[k]);
                            };
                        }
                    });
                };*/
            };
        /*else {if (id2) {
            var value2 = $('#id_genre2-deck').clone().children().children().remove().end().text();
                $.ajax({
                    type:"POST",
                    url: urlUnGenre
                    data: {genre: value2}
                    success:function(tab){
                        for (k=0;k<10;k++) {
                            ajoutKeywordSuggest(tab[k]);
                            };
                        }
                    });
                };
            else {
                $.ajax({
                    type:"POST",
                    url: urlUnGenre
                    data: {genre: value1}
                    
                    success:function(tab){
                          for (k=0;k<10;k++) {
                            ajoutKeywordSuggest(tab[k]);
                            };
                          }
                        
                    });
                };
            };*/
        });
    });
        
            
            
