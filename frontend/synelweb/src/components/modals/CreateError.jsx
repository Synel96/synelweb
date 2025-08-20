import { Modal, ModalDialog, ModalClose, Typography, Button } from "@mui/joy";

function CreateError({ open, onClose }) {
  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="create-error-modal-title"
      aria-modal="true"
      disableScrollLock={false}
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <ModalDialog
        sx={{
          width: { xs: "90vw", sm: 360 },
          maxWidth: "100vw",
          p: { xs: 2, sm: 3 },
          borderRadius: 4,
          boxShadow: "lg",
          backgroundColor: "background.surface",
          textAlign: "center",
        }}
        role="alertdialog"
        aria-labelledby="create-error-modal-title"
      >
        <ModalClose aria-label="Bezárás" />
        <Typography
          id="create-error-modal-title"
          level="h4"
          sx={{ mb: 2, fontWeight: 700 }}
          tabIndex={0}
        >
          Hiányzó kötelező mezők!
        </Typography>
        <Typography level="body1" sx={{ mb: 2 }}>
          A név, az email cím és az értékelés megadása kötelező. Kérjük, töltsd
          ki ezeket a mezőket!
        </Typography>
        <Button
          variant="solid"
          color="primary"
          onClick={onClose}
          sx={{ mt: 1, width: "100%" }}
          aria-label="Bezárás"
        >
          Bezárás
        </Button>
      </ModalDialog>
    </Modal>
  );
}

export default CreateError;
