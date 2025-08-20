import { useState } from "react";
import {
  Modal,
  ModalDialog,
  ModalClose,
  Typography,
  Button,
  Input,
  Textarea,
  Stack,
  FormControl,
  FormLabel,
} from "@mui/joy";
import { postReview } from "../../services/reviewsService";
import CreateError from "./CreateError";
// FontAwesome import
import { FaStar, FaRegStar } from "react-icons/fa";

function StarRating({ value, onChange, max = 5, ...props }) {
  return (
    <div
      role="radiogroup"
      aria-label="Értékelés csillagokkal"
      style={{ display: "flex", gap: 4 }}
      {...props}
    >
      {[...Array(max)].map((_, i) => (
        <button
          key={i}
          type="button"
          aria-label={`${i + 1} csillag`}
          aria-checked={value === i + 1}
          tabIndex={0}
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            padding: 0,
            outline: "none",
            fontSize: "2rem",
            color: "#FFD700",
          }}
          onClick={() => onChange(i + 1)}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              onChange(i + 1);
            }
          }}
        >
          {value > i ? <FaStar /> : <FaRegStar />}
        </button>
      ))}
    </div>
  );
}

function CreateReviewModal({ open, onClose, onSuccess }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showError, setShowError] = useState(false);

  // WCAG: fókuszkezelés a modál megnyitásakor
  const nameInputId = "review-name-input";
  const emailInputId = "review-email-input";
  const ratingInputId = "review-rating-input";
  const commentInputId = "review-comment-input";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    // Ellenőrzés: név, email, értékelés kötelező
    if (!name.trim() || !email.trim() || rating < 1) {
      setShowError(true);
      setLoading(false);
      return;
    }
    setLoading(true);
    try {
      await postReview({ name, email, rating, comment });
      setName("");
      setEmail("");
      setRating(0);
      setComment("");
      setLoading(false);
      if (onSuccess) onSuccess();
      if (onClose) onClose();
    } catch (err) {
      setError("Nem sikerült elküldeni a véleményt.");
      setLoading(false);
    }
  };

  return (
    <>
      <Modal
        open={open}
        onClose={onClose}
        aria-labelledby="create-review-modal-title"
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
            width: { xs: "95vw", sm: 420 },
            maxWidth: "100vw",
            p: { xs: 2, sm: 4 },
            borderRadius: 4,
            boxShadow: "lg",
            backgroundColor: "background.surface",
          }}
          role="dialog"
          aria-labelledby="create-review-modal-title"
        >
          <ModalClose aria-label="Bezárás" />
          <Typography
            id="create-review-modal-title"
            level="h3"
            sx={{
              mb: 2,
              fontSize: { xs: "1.3rem", sm: "1.7rem" },
              fontWeight: 700,
              textAlign: "center",
            }}
            tabIndex={0}
          >
            Vélemény beküldése
          </Typography>
          <form
            onSubmit={handleSubmit}
            aria-describedby={error ? "review-error" : undefined}
          >
            <Stack spacing={2}>
              <FormControl required>
                <FormLabel htmlFor={nameInputId}>Név</FormLabel>
                <Input
                  id={nameInputId}
                  name="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Név"
                  autoFocus
                  required
                  aria-required="true"
                  aria-label="Név"
                  sx={{ width: "100%" }}
                />
              </FormControl>
              <FormControl required>
                <FormLabel htmlFor={emailInputId}>Email cím</FormLabel>
                <Input
                  id={emailInputId}
                  name="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email"
                  required
                  aria-required="true"
                  aria-label="Email cím"
                  sx={{ width: "100%" }}
                />
              </FormControl>
              <FormControl required>
                <FormLabel htmlFor={ratingInputId}>Értékelés</FormLabel>
                <StarRating
                  id={ratingInputId}
                  value={rating}
                  onChange={setRating}
                  max={5}
                  aria-required="true"
                  aria-label="Értékelés csillagokkal"
                />
              </FormControl>
              <FormControl>
                <FormLabel htmlFor={commentInputId}>Vélemény</FormLabel>
                <Textarea
                  id={commentInputId}
                  name="comment"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Írd le a véleményed..."
                  minRows={3}
                  aria-label="Vélemény szövege"
                  sx={{ width: "100%" }}
                />
              </FormControl>
              {error && (
                <Typography
                  id="review-error"
                  color="danger"
                  level="body2"
                  role="alert"
                  sx={{ textAlign: "center" }}
                  tabIndex={0}
                >
                  {error}
                </Typography>
              )}
              <Button
                type="submit"
                loading={loading}
                variant="solid"
                color="primary"
                sx={{
                  mt: 1,
                  width: "100%",
                  fontWeight: 600,
                  fontSize: { xs: "1rem", sm: "1.1rem" },
                }}
                aria-label="Vélemény beküldése"
              >
                Küldés
              </Button>
            </Stack>
          </form>
        </ModalDialog>
      </Modal>
      <CreateError open={showError} onClose={() => setShowError(false)} />
    </>
  );
}

export default CreateReviewModal;
