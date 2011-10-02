$def with (title, err_info=None, static_files=None)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Editing $title</title>

    <style>
    #new_path { width : 400px; }
    </style>

    $if static_files:
        $static_files

</head>
<body>


<div id="container">

<h2>Rename: $title</h2>

<div id="rename">
    <form method="POST" accept-charset="utf-8">
        New name: <input type="text" value="$title" name="new_path" id="new_path" /><br />
        <div id="toolbox">
            <input type="submit" value="Rename" />
        </div>
    </form>
</div>

</div>


</body>
</html>