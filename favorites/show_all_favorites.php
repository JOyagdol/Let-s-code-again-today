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
    $conn->set_charset('utf8');

    //!변수 설정2
    $phone = $conn->real_escape_string($phone);
    
    //!phone에 해당하는 즐겨찾기의 jobid 검색
    try {
        $stmt = $conn->prepare("SELECT jobid FROM favorites WHERE phone = ?");
        $stmt->bind_param("s", $phone);
        $stmt->execute();
        $stmt->store_result();
        $stmt->bind_result($jobid);
        $resultArray = array();

        //!검색된 jobid의 recrtTitle(채용공고), oranNm(기업명) 검색
        while ($stmt->fetch()) {
            $jobid = $conn->real_escape_string($jobid);
            $stmt2 = $conn->prepare("SELECT recrtTitle, oranNm FROM jobs2 WHERE jobid = ?");
            $stmt2->bind_param("s", $jobid);
            $stmt2->execute();
            $stmt2->bind_result($recrtTitle, $oranNm);
            $stmt2->fetch();
            $data = array(
                'recrtTitle' => $recrtTitle,
                'oranNm' => $oranNm,
                'jobid' => $jobid,
            );
            $resultArray[] = $data;
            $stmt2->close();
        }
        $stmt->close();
        $conn->close();
        header('Content-Type: application/json; charset=utf-8');

        echo json_encode($resultArray, JSON_UNESCAPED_UNICODE);
    } catch (Exception $e) {
        echo 'Error: ' . $e->getMessage();
    }
}
?>
