# Contributing to NVIDIA BCM Ansible Collection

Thank you for your interest in contributing to the NVIDIA BCM Ansible Collection!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or request features
- Include BCM version, Ansible version, and RHEL version
- Provide steps to reproduce for bugs
- Include relevant error messages and logs

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/nvidia/ansible-bcm.git
   cd ansible-bcm
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes**
   - Follow the existing code style
   - Update documentation
   - Add tests if applicable

4. **Test your changes**
   ```bash
   # Build the collection
   ansible-galaxy collection build

   # Install locally
   ansible-galaxy collection install nvidia-bcm-*.tar.gz --force

   # Run tests
   ansible-playbook test_all_modules_playbook.yml
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of changes"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/my-new-feature
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

### Module Development

When creating new modules:

1. **Use the template pattern** - See existing modules like `bcm_node.py`
2. **Include comprehensive documentation**:
   - DOCUMENTATION string with all parameters
   - EXAMPLES with practical use cases
   - RETURN with expected output format

3. **Handle errors gracefully**:
   ```python
   try:
       # BCM operation
   except Exception as e:
       module.fail_json(msg=f"Operation failed: {str(e)}")
   ```

4. **Support check mode**:
   ```python
   if not module.check_mode:
       # Make actual changes
   ```

5. **Make operations idempotent**:
   - Check current state before making changes
   - Only commit when changes are needed

### Testing

- Test all query operations
- Test update operations with check mode
- Test error conditions
- Verify idempotency

### Documentation

- Update README.md for new features
- Add examples to playbooks/ directory
- Update QUICKSTART.md if installation changes
- Document any new dependencies

## Module Checklist

Before submitting a new module:

- [ ] Follows existing module pattern
- [ ] Has DOCUMENTATION, EXAMPLES, and RETURN blocks
- [ ] Handles errors gracefully
- [ ] Supports check mode
- [ ] Is idempotent
- [ ] Has been tested with actual BCM instance
- [ ] Documentation is complete
- [ ] Examples are included

## Role Checklist

Before submitting a new role:

- [ ] Has meta/main.yml with proper metadata
- [ ] Has defaults/main.yml with documented variables
- [ ] Has tasks/main.yml with clear task names
- [ ] Has README.md with usage examples
- [ ] Has been tested in a real environment
- [ ] Variables have sensible defaults

## Questions?

- Open a GitHub Discussion for questions
- Check existing issues and pull requests
- Review the DEVELOPMENT.md guide

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0-or-later license.

Thank you for contributing!
