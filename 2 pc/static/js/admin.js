$(document).ready(function() {
    // Handle Manage Users
    $("#manage-users-btn").click(function() {
        // Hide all sections
        hideAllSections();
        
        // Show the manage users section
        $("#manage-users-section").show();
        
        // Fetch users from the backend
        $.ajax({
            url: "/manage_users",
            method: "GET",
            success: function(data) {
                let usersTable = "<table><tr><th>Name</th><th>Email</th><th>Actions</th></tr>";
                data.forEach(user => {
                    usersTable += `<tr><td>${user.name}</td><td>${user.email}</td><td><button class="delete-user" data-id="${user.id}">Delete</button></td></tr>`;
                });
                usersTable += "</table>";
                $("#user-table").html(usersTable);
            },
            error: function(err) {
                alert("Error fetching users: " + err.responseJSON.error);
            }
        });
    });

    // Handle View Audit Logs
    $("#view-audit-logs-btn").click(function() {
        // Hide all sections
        hideAllSections();
        
        // Show the audit logs section
        $("#view-audit-logs-section").show();
        
        // Fetch audit logs from the backend
        $.ajax({
            url: "/view_audit_logs",
            method: "GET",
            success: function(data) {
                let auditTable = "<table><tr><th>User ID</th><th>Activity</th><th>Timestamp</th><th>IP Address</th></tr>";
                data.forEach(log => {
                    auditTable += `<tr><td>${log.user_id}</td><td>${log.activity}</td><td>${log.timestamp}</td><td>${log.ip_address}</td></tr>`;
                });
                auditTable += "</table>";
                $("#audit-logs-table").html(auditTable);
            },
            error: function(err) {
                alert("Error fetching audit logs: " + err.responseJSON.error);
            }
        });
    });

    // Handle Broadcast Message
    $("#broadcast-msg-btn").click(function() {
        // Hide all sections
        hideAllSections();
        
        // Show the broadcast message section
        $("#broadcast-msg-section").show();
    });

    // Send Broadcast Message
    $("#send-broadcast-btn").click(function() {
        let message = $("#broadcast-msg-text").val();
        
        if (!message) {
            alert("Message cannot be empty.");
            return;
        }

        // Send the message via AJAX
        $.ajax({
            url: "/broadcast",
            method: "POST",
            data: { message: message },
            success: function(response) {
                alert(response.message); // Display success message
            },
            error: function(err) {
                alert("Error sending message: " + err.responseJSON.error);
            }
        });
    });

    // Delete User (If implemented in backend)
    $(document).on("click", ".delete-user", function() {
        const userId = $(this).data("id");
        
        // Confirmation before deleting
        if (confirm("Are you sure you want to delete this user?")) {
            $.ajax({
                url: "/delete_user", // You need to implement this route in the backend
                method: "POST",
                data: { user_id: userId },
                success: function(response) {
                    alert(response.message); // Display success message
                    location.reload(); // Reload the page to reflect changes
                },
                error: function(err) {
                    alert("Error deleting user: " + err.responseJSON.error);
                }
            });
        }
    });

    // Helper function to hide all sections
    function hideAllSections() {
        $("#manage-users-section").hide();
        $("#view-audit-logs-section").hide();
        $("#broadcast-msg-section").hide();
    }
});
