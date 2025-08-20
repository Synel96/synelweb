import { Modal, ModalDialog, ModalClose, IconButton } from "@mui/joy";
import { useState } from "react";

function ProjectMediaModal({ open, onClose, images = [], video = "" }) {
  const [activeIdx, setActiveIdx] = useState(0);

  const mediaList = video ? [video, ...images] : images;
  const isVideo = activeIdx === 0 && video;

  const handlePrev = () =>
    setActiveIdx((idx) => (idx > 0 ? idx - 1 : mediaList.length - 1));
  const handleNext = () =>
    setActiveIdx((idx) => (idx < mediaList.length - 1 ? idx + 1 : 0));

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="media-modal-title"
      aria-modal="true"
    >
      <ModalDialog
        sx={{
          minWidth: 320,
          maxWidth: 540,
          p: 2,
          borderRadius: 4,
          boxShadow: "lg",
          backgroundColor: "background.surface",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
        role="dialog"
        aria-labelledby="media-modal-title"
      >
        <ModalClose aria-label="Bezárás" />
        <div style={{ width: "100%", textAlign: "center", marginBottom: 16 }}>
          {isVideo ? (
            <video
              src={video}
              controls
              style={{
                width: "100%",
                maxHeight: 340,
                borderRadius: 8,
                background: "#000",
              }}
            />
          ) : (
            <img
              src={mediaList[activeIdx]}
              alt={`Projekt média ${activeIdx + 1}`}
              style={{
                width: "100%",
                maxHeight: 340,
                objectFit: "contain",
                borderRadius: 8,
                background: "#000",
              }}
            />
          )}
        </div>
        {mediaList.length > 1 && (
          <div style={{ display: "flex", justifyContent: "center", gap: 16 }}>
            <IconButton onClick={handlePrev} aria-label="Előző" color="primary">
              &#8592;
            </IconButton>
            <IconButton
              onClick={handleNext}
              aria-label="Következő"
              color="primary"
            >
              &#8594;
            </IconButton>
          </div>
        )}
      </ModalDialog>
    </Modal>
  );
}

export default ProjectMediaModal;
