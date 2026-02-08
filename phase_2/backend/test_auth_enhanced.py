"""
Test script for enhanced authentication configuration with comprehensive error handling.
"""

import sys
import os
import hashlib
import secrets
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth_enhanced import auth_config, validate_email, validate_password, get_password_hash, verify_password, create_access_token, verify_token
from datetime import timedelta
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_email_validation():
    """Test email validation."""
    logger.info("Testing email validation...")

    # Valid emails
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "user+tag@example.org",
        "user123@test-domain.com"
    ]

    # Invalid emails
    invalid_emails = [
        "invalid-email",
        "@example.com",
        "test@",
        "spaces in@email.com",
        "",
        "missing.tld@"
    ]

    all_passed = True

    # Test valid emails
    for email in valid_emails:
        try:
            is_valid = validate_email(email)
            if is_valid:
                logger.info(f"  ✓ Valid email passed: {email}")
            else:
                logger.error(f"  ✗ Valid email failed: {email}")
                all_passed = False
        except Exception as e:
            logger.error(f"  ✗ Error validating valid email {email}: {str(e)}")
            all_passed = False

    # Test invalid emails
    for email in invalid_emails:
        try:
            is_valid = validate_email(email)
            if not is_valid:
                logger.info(f"  ✓ Invalid email correctly rejected: {email}")
            else:
                logger.error(f"  ✗ Invalid email incorrectly accepted: {email}")
                all_passed = False
        except Exception as e:
            logger.error(f"  ✗ Error validating invalid email {email}: {str(e)}")
            all_passed = False

    return all_passed


def test_password_validation():
    """Test password validation."""
    logger.info("Testing password validation...")

    # Valid passwords
    valid_passwords = [
        "ValidPass1!",
        "AnotherStr0ngP@ssword",
        "MyPass123!@#"
    ]

    # Invalid passwords (too short, missing uppercase, missing digit, missing special char)
    invalid_passwords = [
        ("short", "too short"),
        ("nouppercase1!", "missing uppercase"),
        ("NoDigit!", "missing digit"),
        ("NOLOWERCASE1!", "missing lowercase"),
        ("NoSpecial1", "missing special character"),
    ]

    all_passed = True

    # Test valid passwords
    for pwd in valid_passwords:
        try:
            is_valid, reason = validate_password(pwd)
            if is_valid:
                logger.info(f"  ✓ Valid password passed: {pwd[:5]}...")
            else:
                logger.error(f"  ✗ Valid password failed: {pwd[:5]}... - {reason}")
                all_passed = False
        except Exception as e:
            logger.error(f"  ✗ Error validating valid password: {str(e)}")
            all_passed = False

    # Test invalid passwords
    for pwd, desc in invalid_passwords:
        try:
            is_valid, reason = validate_password(pwd)
            if not is_valid:
                logger.info(f"  ✓ Invalid password correctly rejected ({desc}): {pwd}")
            else:
                logger.error(f"  ✗ Invalid password incorrectly accepted ({desc}): {pwd}")
                all_passed = False
        except Exception as e:
            logger.error(f"  ✗ Error validating invalid password {pwd}: {str(e)}")
            all_passed = False

    return all_passed


def test_password_hashing():
    """Test password hashing and verification."""
    logger.info("Testing password hashing and verification...")

    test_password = "TestPassword123!"

    try:
        # Test hashing
        hashed = get_password_hash(test_password)
        if hashed and len(hashed) > 10:  # Basic check for valid hash
            logger.info("  ✓ Password hashing successful")
        else:
            logger.error("  ✗ Password hashing failed - invalid hash")
            return False

        # Test verification
        is_correct = verify_password(test_password, hashed)
        if is_correct:
            logger.info("  ✓ Password verification successful")
        else:
            logger.error("  ✗ Password verification failed")
            return False

        # Test wrong password
        is_wrong = verify_password("WrongPassword456!", hashed)
        if not is_wrong:
            logger.info("  ✓ Wrong password correctly rejected")
        else:
            logger.error("  ✗ Wrong password incorrectly accepted")
            return False

        # Test with weak password (should raise ValidationError)
        try:
            weak_hash = get_password_hash("weak")
            logger.error("  ✗ Weak password was allowed")
            return False
        except Exception:
            logger.info("  ✓ Weak password correctly rejected")

        return True
    except Exception as e:
        logger.error(f"  ✗ Password hashing/verification test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_token_creation_and_verification():
    """Test token creation and verification."""
    logger.info("Testing token creation and verification...")

    try:
        # Test data
        test_data = {"sub": "test_user_id", "email": "test@example.com"}

        # Create access token
        access_token = create_access_token(test_data)
        if access_token and len(access_token) > 10:
            logger.info("  ✓ Access token creation successful")
        else:
            logger.error("  ✗ Access token creation failed")
            return False

        # Verify access token
        payload = verify_token(access_token)
        if payload and payload.get("sub") == "test_user_id":
            logger.info("  ✓ Access token verification successful")
        else:
            logger.error("  ✗ Access token verification failed")
            return False

        # Create token with custom expiration
        custom_token = create_access_token(test_data, expires_delta=timedelta(minutes=5))
        payload = verify_token(custom_token)
        if payload and payload.get("sub") == "test_user_id":
            logger.info("  ✓ Custom expiration token successful")
        else:
            logger.error("  ✗ Custom expiration token failed")
            return False

        return True
    except Exception as e:
        logger.error(f"  ✗ Token creation/verification test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_config_validation():
    """Test configuration validation."""
    logger.info("Testing configuration validation...")

    try:
        # The auth_config should already be initialized successfully
        # Just test that it has the expected attributes
        attrs_to_check = [
            'oauth2_scheme',
            'validate_email',
            'validate_password',
            'verify_password',
            'get_password_hash',
            'create_access_token',
            'verify_token',
            'get_current_user'
        ]

        for attr in attrs_to_check:
            if hasattr(auth_config, attr):
                logger.info(f"  ✓ Attribute {attr} exists")
            else:
                logger.error(f"  ✗ Attribute {attr} missing")
                return False

        return True
    except Exception as e:
        logger.error(f"  ✗ Configuration validation failed: {str(e)}")
        return False


def run_all_tests():
    """Run all authentication tests."""
    logger.info("Starting comprehensive authentication configuration tests...")

    tests = [
        ("Email Validation", test_email_validation),
        ("Password Validation", test_password_validation),
        ("Password Hashing", test_password_hashing),
        ("Token Creation/Verification", test_token_creation_and_verification),
        ("Config Validation", test_config_validation),
    ]

    results = {}
    for test_name, test_func in tests:
        logger.info(f"\n--- Running {test_name} ---")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {str(e)}")
            traceback.print_exc()
            results[test_name] = False

    # Summary
    logger.info("\n=== Test Summary ===")
    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")

    logger.info(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All authentication tests passed! Enhanced auth configuration is working properly.")
        return True
    else:
        logger.error("❌ Some authentication tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)