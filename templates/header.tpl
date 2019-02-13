<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/css/base.css">
        <link rel="stylesheet" type="text/css" href="/css/sortable-tables.css">
        <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet">
        <script src="/js/sortable-tables.js"></script>

        <meta name="viewport" content="width=device-width, user-scalable=no">
        % if defined('mod'):
            <title>{{ mod['name'] }} - Warframe mods</title>
        % else:
            <title>Warframe mods</title>
        % end
    </head>
    <body>
        <div id="content">
            <input oninput="updateResult(this.value)" type="search" placeholder="search..." />
            <ul class="result">
                <li></li>
            </ul>
