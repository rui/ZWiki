$def with (title, content)
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="utf-8" />
    <title>$title</title>
</head>
<body>

<div id="title">$title</div>

<hr />

<div id="content">$content</div>

<hr />

<div id="toolbox">
<a href="/$title?action=delete">Delete</a>
<a href="/$title?action=rename">Rename</a>
<a href="/$title?action=edit">Edit</a>
</div>

</body>
</html>