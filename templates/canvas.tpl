$def with (title, content, toolbox=True, quicklinks=True)
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8" />
    <title>$title</title>
</head>
<body>


$if quicklinks:
    <div id="quicklinks">
        <a href="/">Recnet Changes</a>
        <a href="/~index">Index</a>
    </div>

    <hr />


<div id="title">$title</div>
<hr />

<div id="content">$content</div>
<hr />

$if toolbox:
    <div id="toolbox">
    <a href="/$title?action=delete">Delete</a>
    <a href="/$title?action=rename">Rename</a>
    <a href="/$title?action=edit">Edit</a>
    </div>


</body>
</html>