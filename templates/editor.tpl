$def with (title, content)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Editing $title</title>
</head>
<body>


<h2>Editing: $title</h2>

<div id="form">
    <form method="POST" accept-charset="utf-8">
        <textarea name="content" cols="100" rows="20">$content</textarea><br>
        <input type="submit" value="Update">
    </form>
</div>


<p><a href="http://daringfireball.net/projects/markdown/syntax">Markdown Syntax</a></p>


</body>
</html>