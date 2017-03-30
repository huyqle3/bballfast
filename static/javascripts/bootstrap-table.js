$(document).ready(function() {
    $('.boxscores-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".boxscores-datatable").wrap("<div class='table-responsive'></div>");
        },

    	paging: false,
    	"bFilter": false,
    	"bInfo" : false,
    	/* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
        	null,
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]},
        	{"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.player-games-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".player-games-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.seasons-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".seasons-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.team-games-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".team-games-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.roster-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".roster-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.coach-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".coach-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.standings-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".standings-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "columnDefs": [
            {
                "targets": 2,
                "orderable": false
            },
            {
                "targets": 4,
                "orderable": false
            },
            {
                "targets": 5,
                "orderable": false
            }
        ],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["asc", "desc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["asc", "desc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.standings-datatable-sm').DataTable({
        "drawCallback": function( settings ) {
            $(".standings-datatable-sm").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "columnDefs": [
            {
                "targets": 2,
                "orderable": false
            },
            {
                "targets": 4,
                "orderable": false
            },
        ],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["asc", "desc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["asc", "desc"]},
            {"orderSequence": ["desc", "asc"]},
        ]
    });
});

$(document).ready(function() {
    $('.body-measurements-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".body-measurements-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.spot-up-shooting-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".spot-up-shooting-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.strength-and-agility-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".strength-and-agility-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.player-vs-player-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".player-vs-player-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});

$(document).ready(function() {
    $('.team-vs-team-datatable').DataTable({
        "drawCallback": function( settings ) {
            $(".player-vs-player-datatable").wrap("<div class='table-responsive'></div>");
        },

        paging: false,
        "bFilter": false,
        "bInfo" : false,
        /* Disable initial sort */
        "aaSorting": [],
        "aoColumns": [
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]},
            {"orderSequence": ["desc", "asc"]}
        ]
    });
});
