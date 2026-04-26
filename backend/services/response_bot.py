import time
import logging
from services.ml_pipeline import ml_pipeline, CLUSTER_METADATA

logger = logging.getLogger(__name__)

RESPONSE_TEMPLATES = {
    0: """Dear {customer_name},

Thank you for contacting us regarding the concern with your credit report. We understand how important accurate credit information is, and we take this matter very seriously.

{t5_summary}

We have initiated a formal investigation into your dispute and will be taking the following steps on your behalf:

{suggested_actions_text}

Please retain your case reference number {account_ref} for all future correspondence. We are required to complete our investigation within 30 days under the Fair Credit Reporting Act (FCRA). You will receive a written confirmation of our findings.

If you have supporting documentation (such as account statements or identity verification documents), please submit them through our secure portal to expedite your case.

Sincerely,
{agent_name}
Credit Disputes Resolution Team
""",

    1: """Dear {customer_name},

Thank you for reaching out to us regarding your experience with debt collection. We take all collection-related concerns seriously and are committed to ensuring that all collection activity complies with the Fair Debt Collection Practices Act (FDCPA).

{t5_summary}

We have placed an immediate hold on all outbound contact to your account pending a thorough investigation. We will be taking the following steps:

{suggested_actions_text}

Your case reference number is {account_ref}. Under the FDCPA, you have the right to request debt validation in writing within 30 days of this notice. If you wish to exercise this right or to dispute the debt, please respond to this letter in writing.

All further communication regarding this matter will be conducted in accordance with federal law.

Sincerely,
{agent_name}
Compliance & Collections Review Team
""",

    2: """Dear {customer_name},

Thank you for contacting us regarding your account and recent billing experience. We appreciate you bringing this to our attention.

{t5_summary}

We have reviewed your account (Reference: {account_ref}) and will be taking the following actions:

{suggested_actions_text}

If any of the identified charges are confirmed to be in error, a credit will be applied to your account within 5 business days. You will receive a detailed account statement confirming any adjustments made.

Should you have any additional questions or require further assistance, please do not hesitate to contact our Account Services team.

Sincerely,
{agent_name}
Account Services & Billing Resolution Team
""",
}


def generate_response(
    complaint_document: dict,
    customer_name: str = "Valued Customer",
    account_ref: str = None,
    agent_name: str = "Customer Relations Team",
) -> dict:
    start = time.time()

    cluster_id = complaint_document["cluster_id"]
    cluster_meta = CLUSTER_METADATA[cluster_id]

    template = RESPONSE_TEMPLATES[cluster_id]
    context = cluster_meta["context"]
    tone = cluster_meta["tone"]
    suggested_actions = cluster_meta["suggested_actions"]

    ref = account_ref or f"CIQ-{complaint_document.get('_id', 'PENDING')}"

    try:
        t5_summary = ml_pipeline.summarize(
            complaint_document["text_clean"],
            max_length=150,
            min_length=60,
        )
    except Exception as e:
        logger.warning(f"T5 summarization failed, using fallback. Error: {e}")
        t5_summary = (
            "We have reviewed the details of your complaint and understand "
            "the inconvenience this situation has caused."
        )

    suggested_actions_text = "\n".join(
        f"  {i + 1}. {action}" for i, action in enumerate(suggested_actions)
    )

    draft_response = template.format(
        customer_name=customer_name,
        account_ref=ref,
        t5_summary=t5_summary,
        suggested_actions_text=suggested_actions_text,
        agent_name=agent_name,
    )

    processing_ms = int((time.time() - start) * 1000)

    return {
        "draft_response": draft_response,
        "response_tone": tone,
        "suggested_actions": suggested_actions,
        "cluster_context": context,
        "confidence": complaint_document["sentiment_confidence"],
        "customer_name": customer_name,
        "account_ref": ref,
        "agent_name": agent_name,
        "cluster_id": cluster_id,
        "cluster_label": cluster_meta["label"],
        "processing_ms": processing_ms,
    }