<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/css/base.css">
        <link rel="stylesheet" type="text/css" href="/css/sortable-tables.css">
        <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet">
        <script src="/js/sortable-tables.js"></script>

        <meta name="viewport" content="width=device-width, user-scalable=no">
        % if defined('item'):
            <title>{{ item['name'] }} - Warframe drops</title>
        % else:
            <title>Warframe drops</title>
        % end
    </head>
    <body>
        <div id="content">
            <input class="search" oninput="updateResult(this.value)" type="search" placeholder="search..." />
            <div class="legend place">Place</div><div class="legend item2">Item</div>
            <div class="search_results">
                <ul class="result">
                    <li></li>
                </ul>
            <div>
