type TextStackProps = {
  lines: string[];
};

export function TextStack({ lines }: TextStackProps) {
  if (lines.length === 0) {
    return <p>No details available yet.</p>;
  }

  return (
    <div className="list-stack">
      {lines.map((line) => (
        <p key={line}>{line}</p>
      ))}
    </div>
  );
}
