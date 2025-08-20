import { useState } from "react";
import { Button } from "@mui/joy";
import CreateReviewModal from "../modals/CreateReviewModal";

function CreateReviewButton({ onSuccess }) {
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <>
      <div
        style={{
          position: "relative",
          display: "inline-block",
          width: "100%",
          maxWidth: "420px",
        }}
      >
        {/* Pulzáló háttér eltávolítva */}
        <Button
          variant="solid"
          color="warning"
          size="lg"
          sx={{
            mt: { xs: 2, sm: 3 },
            mb: { xs: 2, sm: 3 },
            px: { xs: 2, sm: 4 },
            py: { xs: 1.5, sm: 2 },
            fontSize: { xs: "1rem", sm: "1.15rem" },
            fontWeight: 700,
            borderRadius: 4,
            boxShadow: "md",
            width: { xs: "100%", sm: "auto" },
            position: "relative",
            zIndex: 1,
            backgroundColor: "#ff9800", // narancssárga háttér
            color: "#212121", // sötét szöveg, jó kontraszt
            "&:hover": {
              backgroundColor: "#fb8c00", // sötétebb narancs hoverre
            },
          }}
          aria-label="Vélemény írása"
          onClick={handleOpen}
        >
          <span>Mondd el a véleményed a munkámról!</span>
        </Button>
      </div>
      <CreateReviewModal
        open={open}
        onClose={handleClose}
        onSuccess={onSuccess}
      />
    </>
  );
}

export default CreateReviewButton;
