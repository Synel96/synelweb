import { Snackbar, Alert } from "@mui/joy";

function SuccessSnackbar({ open, onClose }) {
  return (
    <Snackbar
      open={open}
      autoHideDuration={4000}
      anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      onClose={onClose}
      variant="soft"
      color="success"
      sx={{
        zIndex: 9999,
        width: { xs: "95vw", sm: "auto" },
        maxWidth: 420,
        borderRadius: 3,
        boxShadow: "md",
      }}
      role="status"
      aria-live="polite"
    >
      <Alert
        variant="soft"
        color="success"
        sx={{
          fontWeight: 600,
          fontSize: { xs: "1rem", sm: "1.05rem" },
          textAlign: "center",
        }}
        onClose={onClose}
        tabIndex={0}
        aria-label="Sikeres beküldés, jóváhagyásra vár"
      >
        Sikeres volt a beküldés, de a véleményed jóváhagyásra vár!
      </Alert>
    </Snackbar>
  );
}

export default SuccessSnackbar;
