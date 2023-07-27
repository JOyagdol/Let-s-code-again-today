<?php
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    //!변수 설정
    $getData = $_GET;
    $phone = $getData['phone'];

    //!db연결
    $conn = new mysqli('localhost', 'root', '1234', 'app');
    if ($conn->connect_error) {
        die('Connection failed: ' . $conn->connect_error);
    }

    //!변수 설정2
    $phone = $conn->real_escape_string($phone);

    //!phone으로 user table에서 나머지 정보 검색
    try {
        $stmt = $conn->prepare("SELECT name, address, career1, career2, hope1 , hope2 FROM user WHERE phone = ?");
        $stmt->bind_param("s", $phone);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            $name = $row['name'];
            $address = $row['address'];
            $career1 = $row['career1'];
            $career2 = $row['career2'];
            $hope1 = $row['hope1'];
            $hope2 = $row['hope2'];
            // JSON 형식으로 데이터 변환
            $data = array(
                "name" => $name,
                "address" => $address,
                "phone" => $phone,
                "career1" => $career1,
                "career2" => $career2,
                "hope1" => $hope1,
                "hope2" => $hope2
            );
            $jsonData = json_encode($data);
            header('Content-Type: application/json');
            echo $jsonData;
        } else {
            echo "No records found for the given phone number.";
        }
    } catch (Exception $e) {
        echo $e->getMessage();
    } finally {
        $stmt->close();
        $conn->close();
    }
}
?>
