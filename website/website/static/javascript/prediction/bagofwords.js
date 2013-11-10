$(document).ready(function() {
var response = new Object();
response = {
    'success': true,
    'error': '',
    'prizes_win': [
        {
            'institution': 'test1',
            'value': 0.3
        },
        {
            'institution': 'test2',
            'value': 0.2
        }
    ],
    'prizes_nomination': [
        {
            'institution': 'test1',
            'value': 0.4
        }
        ,
        {
            'institution': 'test2',
            'value': 0.5
        }
    ],
    'general_box_office': {
        'rank': 24,
        'value': 320,
        'neighbors': [
            {
                'rank': 23,
                'original_title': 'IronMan4',
                'value': 325.5
            },
			{
                'rank': 25,
                'original_title': 'test4',
                'value': 305.5
            }
        ]
    },
    'genre_box_office': {
        'rank': 45,
        'value': 51,
        'neighbors': [
            {
                'rank': 44,
                'original_title': 'IronMan4',
                'value': 325.5
            },
			{
                'rank': 46,
                'original_title': '???',
                'value': 0.5
            }
        ]
    },
    'critics': {
        'average': 0.4
    },
    'reviews': [
        {
            'journal': 'Télérama',
            'grade': 0.60
        },
        {
            'journal': 'Télé7-Jours',
            'grade': 0.18
        }
    ],
	'bag_of_words' : [ 
        {
            'word' : 'amazing',
            'value' : 0.80 
        },
        {
            'word' : 'delightful',
            'value' : 0.70 
        },
		{
            'word' : 'random',
            'value' : 0.10 
        },
		{
            'word' : 'dwhatthefuck',
            'value' : 0.20 
        },
		{
            'word' : 'damn',
            'value' : 0.50 
        },
		{
            'word' : 'justforfun',
            'value' : 0.514159526
        },
		{
            'word' : 'FFFFFFFFFF',
            'value' : 0.65
        },{
            'word' : 'MovieGod',
            'value' : 0.789
        },{
            'word' : 'CRAZY',
            'value' : 0.4562
        },{
            'word' : '0.555',
            'value' : 0.555
        },{
            'word' : 'Killlllllllll',
            'value' : 0.123454
        },{
            'word' : 'AvatarSucks',
            'value' : 0.656
        },{
            'word' : 'Amen',
            'value' : 0.145
        },{
            'word' : 'WhenTheWindBlows',
            'value' : 0.7542
        },{
            'word' : 'DevilGoodIntentions',
            'value' : 0.45698
        },{
            'word' : 'GetOverIt',
            'value' : 0.445
        },
		{
            'word' : 'SCI-FI',
            'value' : 0.8845
        },{
            'word' : 'Space',
            'value' : 0.5412
        },{
            'word' : 'WHYI4MDOINGTHIS§',
            'value' : 0.679
        },{
            'word' : 'Peace',
            'value' : 0.24569
        },
    ]

};

Math.floor((Math.random()*5)+1);
   
	var fill = d3.scale.category20();
    var jWord = [] ;
    var jCount = [];
	var jColor = ["#d51c21","#4d4d4d","#ea5255","#727a86","#a31512","#505864"];
	var length = response.bag_of_words.length;
	for (k=0;k<length;k++) {
		jWord[k] = [response.bag_of_words[k].word];
		jCount[k] = [response.bag_of_words[k].value];
		};
		
    var s = d3.scale.linear().domain([d3.min(jCount),d3.max(jCount)]).range([20, 60]);
    console.log(d3.zip(jWord, jCount));

    d3.layout.cloud().size([420, 340])
        /* .words([
         "Hello", "world", "normallyvrgtrbtnthn", "your", "want", "more", "words",
         "than", "this"].map(function (d) {
         return {text: d, size: 10 + Math.random() * 40};
         }))*/
        .words(d3.zip(jWord, jCount).map(function (d) {
            return {text: d[0], size: s(d[1])};
        }))
        .padding(5)
                .rotate(function () {
                    return ~~(Math.random() * 2) * 90;
                })
                .font("Impact")
                .fontSize(function (d) {
                    return d.size;
                })
                .on("end", draw)
                .start();
	
	function draw(words) {
	    d3.select("#bagofwords").append("svg")
	            .attr("width", 420)
	            .attr("height", 340)
	            .append("g")
	            .attr("transform", "translate(210,170)")
	            .selectAll("text")
	            .data(words)
	            .enter().append("text")
	            .style("font-size", function (d) {
	                return d.size + "px";
	            })
	            .style("font-family", "Impact")
	            .style("fill", function (d, i) {
			
				var value = Math.floor((Math.random()*4)+1);
				
	                return jColor[value];
					
					//return fill(i);
	            })
	            .attr("text-anchor", "middle")
	            .attr("transform", function (d) {
	                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	            })
	            .text(function (d) {
	                return d.text;
	            });
	}
});