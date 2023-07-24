<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // !변수설정
    $postData = json_decode(file_get_contents('php://input'), true);

    $name = $postData['name'];
    $address = $postData['address'];
    $phone = $postData['phone'];
    $career1 = $postData['career1'];
    $career2 = $postData['career2'];
    $hope1 = $postData['hope1'];
    $hope2 = $postData['hope2'];

    //!db연결
    $conn = new mysqli('localhost', 'root', '1234', 'app');
    if ($conn->connect_error) {
        die('Connection failed: ' . $conn->connect_error);
    }

    // !변수설정2
    $name = $conn->real_escape_string($name);
    $address = $conn->real_escape_string($address);
    $phone = $conn->real_escape_string($phone);
    $career1 = $conn->real_escape_string($career1);
    $career2 = $conn->real_escape_string($career2);
    $hope1 = $conn->real_escape_string($hope1);
    $hope2 = $conn->real_escape_string($hope2);

    try {
        $checkSql = "SELECT * FROM user WHERE phone = '$phone'";
        $checkResult = $conn->query($checkSql);

        //!이미 존재하는 phone이면 update
        //!새로운 phone이면 insert
        if ($checkResult->num_rows > 0) {
            $updateSql = "UPDATE user SET name = '$name', address = '$address', career1 = '$career1', career2 = '$career2', hope1 = '$hope1', hope2 = '$hope2' WHERE phone = '$phone'";
            if ($conn->query($updateSql) === true) {
                echo "Form data updated successfully!";
            } else {
                throw new Exception("Error: " . $updateSql . "<br>" . $conn->error);
            }
        } else {
            $insertSql = "INSERT INTO user (name, address, phone, career1,career2, hope1,hope2) VALUES ('$name', '$address', '$phone', '$career1', '$career2', '$hope1', '$hope2')";
            if ($conn->query($insertSql) === true) {
                echo "Form data inserted successfully into the database!";
            } else {
                throw new Exception("Error: " . $insertSql . "<br>" . $conn->error);
            }
        }
    } catch (Exception $e) {
        echo $e->getMessage();
    }
    $conn->close();
}
?>
