<!DOCTYPE HTML>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no">
    <title>Ping-Piesome</title>
    <link rel="stylesheet" type="text/css" href="/i/style">
</head>
<body>
    <div class="world">
        %for group_name in sorted(targets):
        <ul>
            <li>{{ group_name }}</li>
            %for name in sorted(targets[group_name]):
            <li>
                {{ name }}
                <span class="status" data-group="{{ group_name }}" data-name="{{ name }}"></span>
                <span class="rtt" data-group="{{ group_name }}" data-name="{{ name }}"></span>
            </li>
            %end
        </ul>
        %end
        <footer>
            © 2014 Juhani Imberg
            <span class="right">
                cached for 30 seconds •
                <a href="http://github.com/JuhaniImberg/ping-piesome">source</a>
            </span>
        </footer>
    </div>
    <script type="text/javascript" src="/i/script"></script>
</body>
</html>
