<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    //!변수 설정
    $postData = json_decode(file_get_contents('php://input'), true);
    $phone = $postData['phone'];
    $jobid = $postData['jobid'];
    $star = $postData['star'];

    //!db연결
    $conn = new mysqli('localhost', 'root', '1234', 'app');
    if ($conn->connect_error) {
        die('Connection failed: ' . $conn->connect_error);
    }
    
    //!변수 설정2
    $phone = $conn->real_escape_string($phone);
    $jobid = $conn->real_escape_string($jobid);
    $star = $conn->real_escape_string($star);

    //!현제 흰별이면 즐겨찾기 삽입(이후 노란별으로)
    //!현제 노란별이면 즐겨찾기 제거(이후 흰별으로)
    if($star == '흰별'){
        try {
            $stmt = $conn->prepare("INSERT INTO favorites (phone, jobid) VALUES (?, ?)");
            $stmt->bind_param("ss", $phone, $jobid);
            $stmt->execute();
            echo "Data inserted successfully!";
        } catch (Exception $e) {
            echo "Error: " . $e->getMessage();
        } finally {
            $stmt->close();
            $conn->close();
        }
    }else{
        try {
            $stmt = $conn->prepare("DELETE FROM favorites WHERE phone = ? AND jobid = ?");
            $stmt->bind_param("ss", $phone, $jobid);
            $stmt->execute();
    
            if ($stmt->affected_rows > 0) {
                echo "Data deleted successfully!";
            } else {
                echo "No matching data found.";
            }
        } catch (Exception $e) {
            echo "Error: " . $e->getMessage();
        } finally {
            $stmt->close();
            $conn->close();
        }
    }
}
?>
