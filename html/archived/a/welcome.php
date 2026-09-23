<?php
// Enable error reporting for debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Database connection details
$servername = "rm-8psh101b448633zaz.mysql.kualalumpur.rds.aliyuncs.com";
$port = 3306;
$username = "hispeedcity";
$password = "HSCServer@321MY";
$dbname = "hispeed";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname, $port);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Sanitize and validate input data
$action = $_POST['action'] ?? '';
$date_of_registration = $_POST['date_of_registration'] ?? null;
$full_name = $_POST['full_name'] ?? null;
$phone_number = $_POST['phone_number'] ?? null;
$company_name = $_POST['company_name'] ?? null;
$vehicle_number = isset($_POST['vehicle_number']) ? implode(',', $_POST['vehicle_number']) : '';
$vehicle_model = $_POST['vehicle_model'] ?? null;
$vehicle_type = $_POST['vehicle_type'] ?? null;
$vehicle_color = $_POST['vehicle_color'] ?? null;
$staff_id = $_POST['staff_id'] ?? null;
$effective_date = $_POST['effective_date'] ?? null;
$expiry_date = $_POST['expiry_date'] ?? null;
$parking_type = $_POST['parking_type'] ?? null;
$subscription_period = $_POST['subscription_period'] ?? null;
$reason_for_deregistration = $_POST['reason_for_deregistration'] ?? null;

// Debug: Uncomment to check received POST data
// echo '<pre>'; print_r($_POST); echo '</pre>'; exit;

// Prepare SQL statement
$sql = "INSERT INTO parking_registrations 
        (action, date_of_registration, full_name, phone_number, company_name, vehicle_number, vehicle_model, vehicle_type, vehicle_color, staff_id, effective_date, expiry_date, parking_type, subscription_period, reason_for_deregistration) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

$stmt = $conn->prepare($sql);
if ($stmt === false) {
    die("Prepare failed: " . $conn->error);
}

// Bind parameters
$stmt->bind_param("sssssssssssssss", 
    $action, $date_of_registration, $full_name, $phone_number, $company_name, $vehicle_number, $vehicle_model, $vehicle_type, $vehicle_color, $staff_id, $effective_date, $expiry_date, $parking_type, $subscription_period, $reason_for_deregistration
);

// Execute statement
if ($stmt->execute()) {
    echo "Record added successfully.";
} else {
    echo "Error: " . $stmt->error;
}

// Close statement and connection
$stmt->close();
$conn->close();
?>
